from models.baw import barone_adesi_whaley
from models.monte_carlo_sim import monte_carlo
from datetime import datetime
from fredapi import Fred
from pytz import utc
from dotenv import load_dotenv
import os
import yfinance as yf
import numpy as np
from greek_management import manage_greeks

# Get the current date
current_date = datetime.now(utc)

# Set your API key
load_dotenv()
api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)

# Get the 10-year U.S. Treasury yield
data = fred.get_series('GS10')
risk_free_rate = data.iloc[-1] / 100

#Adjust significance based on personal account balance
significance = 0.07

"""
    This function returns a list of option contract symbols to trade on.

    Parameters:
    ticker_symbol (str): The ticker symbol of the stock to trade options on.
    backtest (bool): Whether to run the bot in backtest mode. Default is False. (For backtesting purposes only)
    start_date (str): The start date of the backtest period. (For backtesting purposes only)
    end_date (str): The end date of the backtest period. (For backtesting purposes only)
    freq (str): The frequency of the data. Default is '1d' for daily data. (For backtesting purposes only)

    Returns:
    list: A list of option contract symbols to trade on.
"""
def run_bot(ticker_symbol, backtest=False, start_date=None, end_date=None, freq = '1d'):

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

        if (backtest):
            options_data = ticker.history(start=start_date, end=end_date, interval=freq)

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
                if (volatility <= 0.225):
                    # barone-adesi and whaley model used for low volatility
                    price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'call')

                    # Uncomment for risk management details
                    #manage_greeks(delta, gamma, vega, theta, rho, 100000, 0.5, 10, 0.1, -10)
                else:
                    # monte carlo simulations used for high volatility 
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
                if (volatility <= 0.225):
                    # barone-adesi and whaley model used for low volatility
                    price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'put')
                else:
                    # monte carlo simulations used for high volatility 
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

# Sample Implementation
# list_of_trades = run_bot("AAPL")
# print(list_of_trades)
