import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client
import os
import json

# Replace with your Binance API key and secret
API_KEY = os.getenv('binance_api_key')
API_SECRET = os.getenv('binance_api_secret')

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

def get_historical_data(symbol, interval, limit):
    # Get the historical candlestick data from Binance
    api_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(api_url)
    json_response = response.json()
     
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(json_response, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                              'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                              'taker_buy_quote_asset_volume', 'ignore'])
    data_dict = df.to_dict(orient='records')
    
    with open (f"{symbol}-data.json","w") as json_file:
        json.dump(data_dict, json_file, indent=2)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').sort_values()
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    df.to_csv(f'{symbol}-hist-data.csv', index=False)

    return df

def calculate_moving_averages(data, window_size):
    # Calculate the simple moving average (SMA) and exponential moving average (EMA)
    data['SMA'] = data['close'].rolling(window=window_size).mean()
    data['EMA'] = data['close'].ewm(span=window_size, adjust=False).mean()

    return data

def plot_technical_analysis(data):
    # Plot the closing prices, SMA, and EMA
    plt.plot(data['timestamp'], data['close'], label='Closing Price')
    plt.plot(data['timestamp'], data['SMA'], label='Simple Moving Average (SMA)')
    plt.plot(data['timestamp'], data['EMA'], label='Exponential Moving Average (EMA)')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Moving Averages Technical Analysis')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Define the symbol, interval, and limit for the historical data
symbol = 'BTCUSDT'  # Replace with your desired trading pair
interval = '1d'    # Replace with your desired interval (e.g., 1m, 5m, 1h, 1d)
limit = 200        # Replace with the number of candles you want to retrieve

# Get the historical data
historical_data = get_historical_data(symbol, interval, limit)

# Calculate the moving averages
window_size = 20 

# print(historical_data)
