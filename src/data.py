import yfinance as yf
import numpy as np

def download_data(stocks, start, end):
    data = yf.download(stocks, start=start, end=end, interval="1d", auto_adjust=True)["Close"]
    data = data.sort_index()
    return np.log(data)
