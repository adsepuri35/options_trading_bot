import alpaca_trade_api as tradeapi
from models.baw import barone_adesi_whaley

# Initialize the Alpaca API
api = tradeapi.REST('APCA-API-KEY-ID', 'APCA-API-SECRET-KEY', base_url='https://paper-api.alpaca.markets')

# Define your trading parameters
symbol = 'AAPL'
strike_price = 100
risk_free_rate = 0.05
dividend_yield = 0.02
time_to_expiration = 0.8
volatility = 0.3
option_type = 'call'

# Get the current stock price
current_price = api.get_last_trade(symbol).price

# Calculate the option price using the Barone-Adesi Whaley model
price, delta, gamma, vega, theta, rho = barone_adesi_whaley(current_price, strike_price, risk_free_rate, dividend_yield, time_to_expiration, volatility, option_type)

# If the model's price is significantly higher than the market price, buy the option
if price > current_price * 1.05:
    api.submit_order(
        symbol=symbol,
        qty=1,
        side='buy',
        type='market',
        time_in_force='gtc'
    )