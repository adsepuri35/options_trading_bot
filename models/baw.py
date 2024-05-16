import math
from scipy.stats import norm
import numpy as np

def barone_adesi_whaley(S, X, r, q, T, sigma, option_type):
    """
    Calculates the price, delta, gamma, vega, theta, and rho of an option using the Barone-Adesi and Whaley approximation model.

    Parameters:
    - S (float): Stock price
    - X (float): Strike price
    - r (float): Risk-free interest rate
    - q (float): Dividend yield
    - T (float): Time to expiration (in years)
    - sigma (float): Volatility
    - option_type (str): Option type ('call' or 'put')

    Returns:
    - price (float): Option price
    - delta (float): Option delta - The sensitivity of the option price to changes in the underlying asset price
    - gamma (float): Option gamma - The sensitivity of the option delta to changes in the underlying asset price
    - vega (float): Option vega - The sensitivity of the option price to changes in the volatility of the underlying asset
    - theta (float): Option theta - The sensitivity of the option price to changes in the time to expiration
    - rho (float): Option rho - The sensitivity of the option price to changes in the risk-free interest rate
    """
    d1 = (math.log(S / X) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        alpha = (-(r - q) + np.sqrt((r - q)**2 + 2 * r * sigma**2)) / (sigma**2)
        beta = (-(r - q) - np.sqrt((r - q)**2 + 2 * r * sigma**2)) / (sigma**2)
        h1 = -(r - q) * T + 2 * sigma * np.sqrt(T) * d1
        h2 = -(r - q) * T + 2 * sigma * np.sqrt(T) * d2
        price = (S * np.exp(-q * T) * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2) +
                 (S * np.exp(-q * T) * (h1 / (1 + h1)) * norm.cdf(alpha) -
                  X * np.exp(-r * T) * (h2 / (1 + h2)) * norm.cdf(beta)))
        delta = np.exp(-q * T) * norm.cdf(d1)
        gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
        theta = -(S * sigma * np.exp(-q * T) * norm.pdf(d1)) / (2 * np.sqrt(T)) - q * S * np.exp(-q * T) * norm.cdf(d1) + r * X * np.exp(-r * T) * norm.cdf(d2)
        rho = X * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        alpha = (-(r - q) - np.sqrt((r - q)**2 + 2 * r * sigma**2)) / (sigma**2)
        beta = (-(r - q) + np.sqrt((r - q)**2 + 2 * r * sigma**2)) / (sigma**2)
        h1 = -(r - q) * T - 2 * sigma * np.sqrt(T) * d1
        h2 = -(r - q) * T - 2 * sigma * np.sqrt(T) * d2
        price = (X * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1) +
                 (X * np.exp(-r * T) * (h2 / (1 - h2)) * norm.cdf(-beta) -
                  S * np.exp(-q * T) * (h1 / (1 - h1)) * norm.cdf(-alpha)))
        delta = -np.exp(-q * T) * norm.cdf(-d1)
        gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
        theta = -(S * sigma * np.exp(-q * T) * norm.pdf(d1)) / (2 * np.sqrt(T)) + q * S * np.exp(-q * T) * norm.cdf(-d1) - r * X * np.exp(-r * T) * norm.cdf(-d2)
        rho = -X * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    return price, delta, gamma, vega, theta, rho

# # Example usage
# S = 100  # Stock price
# X = 102  # Strike price
# r = 0.05  # Risk-free interest rate
# q = 0.02  # Dividend yield
# T = 0.8  # Time to expiration (in years)
# sigma = 0.15  # Volatility
# option_type = 'call'  # Option type ('call' or 'put')

# price, delta, gamma, vega, theta, rho = barone_adesi_whaley(S, X, r, q, T, sigma, option_type) 
# print("Option price:", price)
# print("Delta:", delta)
# print("Gamma:", gamma)
# print("Vega:", vega)
# print("Theta:", theta)
# print("Rho:", rho)