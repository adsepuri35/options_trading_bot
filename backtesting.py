
import math
from scipy.stats import norm
import pandas as pandas
from datetime import datetime
from models.baw import barone_adesi_whaley
import yfinance as yf


def backtest_option(symbol, startD, endD, freq = '1d'):
    data = yf.download(symbol, start=startD, end=endD, interval=freq)
    numTrades = 0
    numWin = 0
    numLose = 0
    totalProfit = 0
    for index, row in data.iterrows():
        S = row['Close'] # Stock price
        X = 100 # Strike price
        r = 0.01 # Risk-free interest rate
        q = 0.01 # Dividend yield
        T = (endD - index).days / 365.0 # Time to expiration (in years)
        sigma = 0.2 # Volatility
        optionT = 'put'
        price, delta, gamma, vega, theta, rho = barone_adesi_whaley(S, X, r, q, T, sigma, optionT)
        print(f"Price: {price}, Delta: {delta}, Gamma: {gamma}, Vega: {vega}, Theta: {theta}, Rho: {rho}")
        
        numTrades += 1
        tradeProfit = price - S #if u buy the option at closing price
        totalProfit += tradeProfit
        if tradeProfit > 0:
            numWin += 1
        else:
            numLose += 1
    print("************************************************")
    print(f"Total trades: {numTrades}")
    print(f"Winning trades: {numWin}")
    print(f"Losing trades: {numLose}")
    print(f"Total profit: {totalProfit}")

symbol = 'AAPL'
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

backtest_option(symbol, start_date, end_date)

#calc the profit and count winning and losing trades