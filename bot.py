from models.baw import barone_adesi_whaley
from models.monte_carlo_sim import monte_carlo
import yfinance as yf
from datetime import datetime
from fredapi import Fred
from pytz import utc
import numpy as np

# Get the current date
current_date = datetime.now(utc)

# Set your API key
fred = Fred(api_key='a960e3f5850c128c7669ac7a257703ab')
# Get the 10-year U.S. Treasury yield
data = fred.get_series('GS10')
risk_free_rate = data.iloc[-1] / 100

significance = 0.07

"""
    This function returns a list of option contract symbols to trade on.

    Parameters:
    ticker_symbol (str): The ticker symbol of the stock to trade options on.
    model (str): The model to use for deciding which options to trade.

    Returns:
    list: A list of option contract symbols to trade on.
"""
def run_bot(ticker_symbol, model):

    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Check Ticker validity
    if ticker.history(period="1d").empty:
        print(f"Invalid ticker symbol: {ticker_symbol}")
        return

    # See if dividend yield available
    try:
        dividend_yield = ticker.info['dividendYield']
    except KeyError:
        print(f"No dividend yield available for {ticker_symbol}")
        return

    good = 0
    bad = 0

    trades = []

    for expiration_date in ticker.options:
        options_data = ticker.option_chain(expiration_date)

        # The option_chain method returns a named tuple with two dataframes: calls and puts
        calls = options_data.calls
        puts = options_data.puts

        # Convert expiration_date from string to datetime and make it offset-aware
        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').replace(tzinfo=utc)

        # Calculate time to expiration
        time_to_expiration = (expiration_date - current_date).days / 365.0

        if time_to_expiration <= 0:
            continue

        for index, row in calls.iterrows():
            option_id = row['contractSymbol']
            strike = row['strike']
            lastPrice = row['lastPrice']
            volatility = row['impliedVolatility']
            
            try:
                if (model == "baw"):
                    price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'call')
                elif (model == "mc"):
                    price = monte_carlo(lastPrice, strike, risk_free_rate, volatility, time_to_expiration, 1000, 'call')

                if price > lastPrice * (1 + significance):
                    good += 1
                    trades.append(option_id)
                else:
                    bad += 1
            except Exception as e:
                print(f"Error calculating option price for strike {strike}: {e}")
                continue

        for index, row in puts.iterrows():
            option_id = row['contractSymbol']
            strike = row['strike']
            lastPrice = row['lastPrice']
            volatility = row['impliedVolatility']
            
            try:
                if (model == "baw"):
                    price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'put')
                elif (model == "mc"):
                    price = monte_carlo(lastPrice, strike, risk_free_rate, volatility, time_to_expiration, 1000, 'put')

                if price < lastPrice * (1 - significance):
                    good += 1
                    trades.append(option_id)
                else:
                    bad += 1
            except Exception as e:
                print(f"Error calculating option price for strike {strike}: {e}")
                continue

    # print(good)
    # print(bad)

    return trades

# # Sample Implementation
# list_of_trades = run_bot("AAPL", "baw")
# print(list_of_trades)
