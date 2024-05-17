import numpy as np
import pandas as pandas
import yfinance as yf
from scipy.stats import norm
from datetime import datetime
from bot import run_bot

def backtest_bot(symbol, startD, endD, freq = '1d'):
    data = yf.download(symbol, start=startD, end=endD, interval=freq)
    numTrades = 0
    numWin = 0
    numLose = 0
    totalProfit = 0
    for index, row in data.iterrows():
        S = row['Close'] # Stock price
        option_ids = run_bot(symbol, True, startD, endD, freq) # Run the bot to get the option ids

        for option_id in option_ids:
            # Fetch the option
            option = None
            ticker = yf.Ticker(symbol)
            for expiration_date in ticker.options:
                options = ticker.option_chain(expiration_date)
                option = options.calls[options.calls['contractSymbol'] == option_id]
                if not option.empty:
                    break

            if option is not None and not option.empty:
                numTrades += 1
                tradeProfit = option['lastPrice'].values[0] - S #if u buy the option at closing price
                totalProfit += tradeProfit
                if tradeProfit > 0:
                    numWin += 1
                else:
                    numLose += 1

    return numTrades, numWin, numLose, totalProfit

# Example usage
# symbol = 'AAPL'
# start_date = '2023-01-01'
# end_date = '2023-12-31'

# numTrades, numWin, numLose, totalProfit = backtest_bot(symbol, start_date, end_date)

# print("************************************************")
# print(f"Total trades: {numTrades}")
# print(f"Winning trades: {numWin}")
# print(f"Losing trades: {numLose}")
# print(f"Total profit: {totalProfit}")