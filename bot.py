from models.baw import barone_adesi_whaley
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

# Function that returns list of options to make a trade on with associated option id's
def run_bot(ticker_symbol):

    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get dividend yield & check Ticker validity
    try:
        dividend_yield = ticker.info['dividendYield']
    except KeyError:
        print(f"Invalid ticker symbol: {ticker_symbol}")
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
                price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'call')

                if price > lastPrice * 1.05:
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
                price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'put')

                if price < lastPrice * 0.95:
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
