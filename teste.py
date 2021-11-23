import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf #https://pypi.org/project/yfinance/
import altair as alt

aapl = yf.Ticker("MSFT")
days = 20
hist = (aapl.history(period=f"{days}d")) # period= serve pra selecionar a data que quer

#print(hist.columns)

#print(hist.reset_index()) # coloca index

hist_msft = yf.Ticker("MSFT").history(period=f"{days}d")
#print(hist_msft.head())

#print(hist.head(3))
#print(hist.index)

# datetime -> str
hist.index = hist.index.strftime("%d %B %Y")
#print(hist.index)
#print(hist.head())

#apple の株
hist = hist[["Close"]]
hist.columns = ["apple"]
#print(hist.head())

# Inverte a posicao dos dados
hist = hist.T
#print(hist)

#　cria name como uma index
hist.index.name = "Name"
#print(hist)

tickers = {"apple":"AAPl",
           "facebook":"FB",
           "bitcoin":"BTC-USD",
           "microsoft":"MSFT",
           "netflix":"NFLX",
           "amazon":"AMZN"

          }
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

print(get_data(days,tickers)) #recebe dia e os tickers
#print(aapl.info) 株情報
#print(aapl.actions.head())