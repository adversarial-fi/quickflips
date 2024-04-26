import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from termcolor import colored

# Hardcoded API Keys
CRYPTOCOMPARE_API_KEY = "YOUR-CRYPTOCOMPARE-API-KEY-GOES-HERE"
API_KEY = "YOUR-BASESCAN-API-KEY-GOES-HERE"

# Prompt for the path to the CSV file
addresses_file_path = input("Enter the path to your CSV file with addresses: ")

# Function to get the current ETH to USD rate
def get_eth_to_usd():
    url = f"https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&api_key={CRYPTOCOMPARE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['USD']

# Read addresses from CSV
try:
    addresses = pd.read_csv(addresses_file_path, header=None).squeeze().tolist()
except Exception as e:
    print(f"Failed to read addresses: {e}")
    exit()

BASE_URL = "https://api.basescan.org/api"

def fetch_trades(address):
    """Fetch trades for the given address over the past 31 days."""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=31)
    url = f"{BASE_URL}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Check for errors or unexpected format in the API response
    if 'result' not in data or not isinstance(data['result'], list):
        print(f"Unexpected API response for address {address}: {data}")
        return pd.DataFrame() # Return an empty DataFrame to avoid errors
    
    # Attempt to create a DataFrame
    try:
        df = pd.DataFrame(data['result'])
        # Convert timestamps and filter dates
        df['timeStamp'] = pd.to_datetime(df['timeStamp'].astype(int), unit='s')
        df = df[(df['timeStamp'] >= start_date) & (df['timeStamp'] <= end_date)]
        # Select and rename columns, convert Ether values
        df = df[['timeStamp', 'from', 'to', 'hash', 'value']]
        df.columns = ['Time', 'Address', 'Contract', 'TXID', 'ETH Amount']
        df['ETH Amount'] = pd.to_numeric(df['ETH Amount'], errors='coerce') / 10**18
    except Exception as e:
        print(f"Error processing data for address {address}: {e}")
        return pd.DataFrame() # Return empty DataFrame in case of an error
    
    return df

all_trades = []

# Get the current ETH to USD conversion rate
eth_to_usd_rate = get_eth_to_usd()

for address in addresses:
    print(f"Fetching trades for address: {address}")
    df = fetch_trades(address)
    if not df.empty:
        all_trades.append(df)

if all_trades:
    # Combine all trades into a single DataFrame
    all_trades_df = pd.concat(all_trades, ignore_index=True)

    # Generate new filename based on original path with timestamp
    base, ext = os.path.splitext(addresses_file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Format the timestamp
    output_path = f"{base}_trades_{timestamp}{ext}" # Insert the timestamp into the file name

    # Export to CSV
    all_trades_df.to_csv(output_path, index=False)
    print(f"Data exported successfully to {output_path}")

    # Analyzing the most constant traders
    top_traders = all_trades_df['Address'].value_counts().nlargest(5)
    print(colored("Top 5 addresses with the most constant trades:", 'green'))
    for address, count in top_traders.items():
        print(colored(f"Address: {address}", 'yellow'))
        print(colored(f"Trades Count: {count}", 'blue'))
        print("Zerion History Link: " + colored(f"https://app.zerion.io/{address}/history", 'cyan'))

        # Additional metrics
        avg_trade_size = all_trades_df[all_trades_df['Address'] == address]['ETH Amount'].mean()
        total_volume = all_trades_df[all_trades_df['Address'] == address]['ETH Amount'].sum()
        trade_frequency = all_trades_df[all_trades_df['Address'] == address]['Time'].count()

        print(colored(f"Average Trade Size: {avg_trade_size:.4f} ETH (${avg_trade_size * eth_to_usd_rate:.2f})", 'magenta'))
        print(colored(f"Total Trade Volume: {total_volume:.4f} ETH (${total_volume * eth_to_usd_rate:.2f})", 'magenta'))
        print(colored(f"Trade Frequency: {trade_frequency} trades", 'magenta'))

        # Most profitable trade
        max_trade = all_trades_df[all_trades_df['Address'] == address].nlargest(1, 'ETH Amount')
        if not max_trade.empty:
            max_value = max_trade.iloc[0]['ETH Amount']
            txid = max_trade.iloc[0]['TXID']
            print(colored(f"Most Profitable Trade: {max_value} ETH (${max_value * eth_to_usd_rate:.2f})", 'green'))
            print("Transaction Link: " + colored(f"https://basescan.org/tx/{txid}", 'cyan'))
            print(colored(f"----------------------------------------------------------------------------------------------------", 'white'))
        else:
            print(colored("No profitable ETH trade found for this address.", 'red'))
else:
    print("No data available to concatenate and export.")
