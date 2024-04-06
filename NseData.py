import requests
import json

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_5min&symbol=IDEA&interval=5min&apikey=9YRAEWS4VNXK6400'

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Save the data to a new file (e.g., 'reliance_data.json')
    with open('reliance_data.json', 'w') as json_file:
        json.dump(data, json_file)

    print("Data saved successfully.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
