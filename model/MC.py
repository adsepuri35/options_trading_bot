import numpy as np

def monte_carlo(S0, K, r, sigma, T, num_paths, option_type):
    """
    Calculate the option price using Monte Carlo simulation.
    
    Parameters:
    S0 (float): Initial stock price
    K (float): Strike price
    r (float): Risk-free interest rate
    sigma (float): Volatility of the underlying asset
    T (float): Time to maturity (in years)
    num_paths (int): Number of Monte Carlo paths
    option_type (str): 'call' or 'put'
    
    Returns:
    float: Option price
    """
    
    # Define the time step
    dt = T / 252  # Assuming 252 trading days per year
    
    # Generate random paths
    paths = np.zeros((num_paths, 252))
    paths[:, 0] = S0
    for t in range(1, 252):
        z = np.random.standard_normal(num_paths)
        paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    # Calculate payoffs at expiration
    if option_type == 'call':
        payoffs = np.maximum(paths[:, -1] - K, 0)
    else:
        payoffs = np.maximum(K - paths[:, -1], 0)
    
    # Discount and average
    discount_factor = np.exp(-r * T)
    option_price = discount_factor * payoffs.mean()
    
    return option_price

# Example usage
S0 = 100  # Initial asset price
K = 102  # Strike price
r = 0.05  # Risk-free rate
sigma = 0.3  # Volatility
T = 0.8  # Time to expiration
N = 1000  # Number of paths
option_type = 'call'  # Option type ('call' or 'put')

option_price = monte_carlo(S0, K, r, sigma, T, N, option_type)
print(f"Estimated option price: {option_price}")