import pandas as pd
import yfinance as yf #https://pypi.org/project/yfinance/
import altair as alt
import streamlit as st

st.title("株価可視化アプリ")

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションを選択
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider("日数",1,50,20)

st.write(f"""
### 過去 **{days}日間**のGAFA株価
""")

@st.cache #cache にためて高速化のため
def get_data(days,tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
    #company = "facebook"
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days}d") # period= serve pra selecionar a data que quer
        hist.index = hist.index.strftime("%d %B %Y")
        hist = hist[["Close"]]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"
        df = pd.concat([df,hist])#df　に　histを入れる
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲設定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください',
        0.0, 3500.0,(0.0 ,4500.0)
    )

    tickers = {"apple":"AAPl",
               "facebook":"FB",
               "bitcoin":"BTC-USD",
               "microsoft":"MSFT",
               "netflix":"NFLX",
               "amazon":"AMZN"

    }

    df = get_data(days,tickers)
    companies = st.multiselect(
        "会社名を選択してください",
        list(df.index), #リストに変換
        ["apple","microsoft","amazon"] #デフォルト値
    )
    if not companies:
        st.error("少なくとも一社を選んでください。")
    else:
        data = df.loc[companies]
        st.write("### 株価",data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data,id_vars=["Date"]).rename(
            columns={"value":"Stock Prices(USD)"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8,clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale( domain=[ymin, ymax] ) ),
                color='Name:N'
            )
        )
        st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        "ERROR"
    )
