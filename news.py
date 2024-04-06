import requests
import json

ALPHA_VANTAGE_API_KEY = '9YRAEWS4VNXK6400'
symbol = 'VODA.L'  # Replace with the stock symbol

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}'

response = requests.get(url)
data = response.json()

file_path = 'stock_news_data.json'

with open(file_path, 'w') as json_file:
    json.dump(data, json_file)

print(f"Stock news data saved to {file_path}")
