# Options Trading Bot

This project is an options trading bot for standard American stock options that uses advanced models and techniques to make profitable trades in both low and high volatility markets. The bot is designed to be flexible, efficient, and easy to deploy and maintain.

## Models

### Barone-Adesi and Whaley Pricing Model

The Barone-Adesi and Whaley model is ananalytical approximation method for pricing American options and was introduced as an extension of the Black-Scholes model, aiming to account for the early exercise premium of American options.

The value of the trade is given by:
![BAW Value](./images/baw1.png)

where:

![BAW Reference](./images/baw2.png)

Reference: https://assets.pubpub.org/or0zyxly/21654278914381.pdf

The BAW model uses a quadratic approximation to the early exercise boundary, which allows for a closed-form solution for the option price. This makes the model computationally efficient and suitable for pricing American options on non-dividend-paying stocks and indices.
In low volatility environments, the BAW model is known to perform well for several reasons:

1. **Accuracy**: The quadratic approximation used in the BAW model works particularly well when the early exercise premium is small, which is typically the case in low volatility markets. The model's accuracy in these conditions is generally comparable to more computationally intensive numerical methods.
2. **Computational Efficiency**: The closed-form solution of the BAW model makes it computationally efficient, allowing for fast pricing and easy integration into trading systems or real-time applications.
3. **Stability**: The model's behavior is relatively stable in low volatility regimes, providing consistent and reliable pricing results.

However, it's important to note that the BAW model can become less accurate in high volatility environments or when the underlying asset pays significant dividends. In such cases, alternative methods like binomial trees or Monte Carlo simulations may be more appropriate.

### Monte Carlo Simulations

Monte Carlo simulations are a computational technique used to estimate the value of an option or other derivative by simulating the future behavior of the underlying asset. This method is particularly useful in high volatility environments where analytical models may struggle to accurately capture the complexities of the market dynamics.

Example of Monte Carlo Simulations for Standard Stock Price (Not Options):
![MC Example](./images/mc_sim.png)

Reference: https://www.tejwin.com/en/insight/options-pricing-with-monte-carlo-simulation/

In a Monte Carlo simulation for option pricing, the following steps are typically followed:
1. **Generate Random Paths**: A large number of possible future price paths for the underlying asset are generated using random variables and a stochastic process model (e.g., Geometric Brownian Motion).
2. **Calculate Payoffs**: For each simulated price path, the payoff of the option is calculated at the expiration date based on the contractual terms.
3. **Discount and Average**: The payoffs from all simulated paths are discounted back to the present value using an appropriate risk-free rate, and the average of these discounted payoffs is taken as an estimate of the option's current fair value.

Monte Carlo simulations perform well in high volatility environments for several reasons:
1. **Flexibility**: Monte Carlo methods can handle a wide range of option styles, underlying asset dynamics, and path-dependent payoff structures, making them suitable for complex derivative products.
2. **Capture of Volatility Dynamics**: By simulating the underlying asset's price paths directly, Monte Carlo simulations can accurately capture the effects of high volatility, including jumps, stochastic volatility, and other non-standard dynamics.
3. **Convergence**: With a sufficiently large number of simulated paths, Monte Carlo simulations can converge to the true option value, providing reliable results even in highly volatile market conditions.

## Features

- **Low Volatility Trading**: For low volatility markets, the bot utilizes the Barone-Adesi and Whaley (BAW) model, a popular and effective approach for pricing American options.

- **High Volatility Trading**: In high volatility market conditions, the bot employs Monte Carlo simulations to estimate option prices and make trading decisions more accurately.

- **Backtesting Engine**: A powerful backtesting engine is included, allowing you to evaluate the performance of your trading strategies on historical market data before deploying them in live markets.

- **Risk Management**: The bot calculates and provides essential Greeks (Delta, Gamma, Vega, Theta, and Rho) for effective risk management and position adjustment.

- **Docker Containerization**: The entire project can be packaged and deployed as a Docker container, ensuring consistent and reproducible behavior across different environments.

## Getting Started

Follow these steps to set up and run the options trading bot:

1. Clone the repository:
git clone https://github.com/your-username/options-trading-bot.git

2. Build the Docker image:
docker build -t options-trading-bot .

3. Run the Docker container:
docker run -it options-trading-bot

4. Configure the bot by modifying the `config.py` file with your desired settings, such as trading parameters, data sources, and broker credentials.

5. Run the bot:
python bot.py

## Contributing

Contributions are welcome! If you find any issues or want to enhance the project, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
