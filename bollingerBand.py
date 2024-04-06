import pandas as pd
import json
import plotly.graph_objects as go

def calculate_bollinger_bands(df, window=20, num_std=2):
    # Calculate rolling mean and standard deviation
    df['MA'] = df['4. close'].rolling(window=window).mean()
    df['Upper'] = df['MA'] + (df['4. close'].rolling(window=window).std() * num_std)
    df['Lower'] = df['MA'] - (df['4. close'].rolling(window=window).std() * num_std)
    return df

def plot_candlestick_with_bollinger_bands(df):
    fig = go.Figure()

    # Add candlestick trace
    fig.add_trace(go.Candlestick(x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'],
                name='Candlestick'))

    # Add Bollinger Bands traces
    fig.add_trace(go.Scatter(x=df.index, y=df['Upper'], mode='lines', name='Upper Bollinger Band', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA'], mode='lines', name='20-day Moving Average', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Lower'], mode='lines', name='Lower Bollinger Band', line=dict(color='green')))

    # Customize layout
    fig.update_layout(title='Candlestick with Bollinger Bands (Intraday)',
                      xaxis_title='Time',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)

    # Show the interactive plot
    fig.show()

def main():
    # Read the JSON data from the file
    file_path = 'reliance_data.json'  # Replace with the actual path
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract intraday time series data
    intraday_data = data['Time Series (1min)']

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(intraday_data).T
    df.index = pd.to_datetime(df.index)

    # Sort DataFrame by time
    df.sort_index(inplace=True)

    # Calculate Bollinger Bands for the intraday data
    df = calculate_bollinger_bands(df)

    # Plot candlestick chart with Bollinger Bands
    plot_candlestick_with_bollinger_bands(df)

# if __name__ == "__main__":
#     main()



