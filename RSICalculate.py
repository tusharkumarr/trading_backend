def calculate_rsi(closing_prices, lookback=14):
  """Calculates the RSI for a given list of closing prices using the specified lookback period.

  Args:
      closing_prices: A list of closing prices (floats).
      lookback: The number of periods to consider for the calculation (default: 14).

  Returns:
      A list of RSI values corresponding to the closing prices.
  """
  rsi_values = []
  for i in range(len(closing_prices)):
    if i < lookback - 1:
      rsi_values.append(None)  # No RSI for initial periods
    else:
      average_gain = 0
      average_loss = 0
      for j in range(1, lookback + 1):
        price_change = closing_prices[i] - closing_prices[i - j]
        if price_change > 0:
          average_gain += price_change
        else:
          average_loss += abs(price_change)  # Use absolute value for losses

      if average_loss == 0:  # Avoid division by zero
        rs = float('inf')  # Relative Strength becomes infinity
      else:
        rs = average_gain / average_loss

      rsi_value = 100 - (100 / (1 + rs))
      rsi_values.append(rsi_value)
  return rsi_values

# Extract closing prices from historical data
# closing_prices = [day["close"] for day in historical_data]

# Calculate RSI using your preferred lookback period (typically 14)
closing_prices = [140, 138, 142, 139, 145, 137, 141, 136, 143,150,120,160,140,158,165,169,153,698]
# rsi_values = calculate_rsi(closing_prices)

# Use the RSI values for your analysis or visualization
# print(rsi_values[-5::])
import nsetools
def get_stocks_list():
  

# Get a list of Nifty 50 companies
    index = "nifty50"
    index_data = nsetools.get_index_pe(index)
    nifty_companies = index_data["data"][index]["companies"]

    print(nifty_companies)

get_stocks_list()
