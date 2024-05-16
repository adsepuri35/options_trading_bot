from models.baw import barone_adesi_whaley
import yfinance as yf
from datetime import datetime

# Get the current date
current_date = datetime.now()

# Define the ticker symbol for the stock you're interested in
ticker_symbol = 'AAPL'

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Get options data
options_data = ticker.option_chain()

# The option_chain method returns a named tuple with two dataframes: calls and puts
calls = options_data.calls
puts = options_data.puts

# Now you can access data about the call options and put options
print(calls)
print(puts)

risk_free_rate = 0.05
# Get dividend yield
dividend_yield = ticker.info['dividendYield']

for index, row in calls.iterrows():
    strike = row['strike']
    lastPrice = row['lastPrice']
    volatility = row['impliedVolatility']
    time_to_expiration = (calls['lastTradeDate'] - current_date).dt.days / 365.0
    price, delta, gamma, vega, theta, rho = barone_adesi_whaley(lastPrice, strike, risk_free_rate, dividend_yield, time_to_expiration, volatility, 'call')


# # Define your trading parameters
# symbol = 'AAPL'
# strike_price = 100
# risk_free_rate = 0.05
# dividend_yield = 0.02
# time_to_expiration = 0.8
# volatility = 0.3
# option_type = 'call'

# # Get the current stock price
# current_price = api.get_last_trade(symbol).price

# # Calculate the option price using the Barone-Adesi Whaley model
# price, delta, gamma, vega, theta, rho = barone_adesi_whaley(current_price, strike_price, risk_free_rate, dividend_yield, time_to_expiration, volatility, option_type)

# # If the model's price is significantly higher than the market price, buy the option
# if price > current_price * 1.05:
#     api.submit_order(
#         symbol=symbol,
#         qty=1,
#         side='buy',
#         type='market',
#         time_in_force='gtc'
#     )