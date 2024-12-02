import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import time
import pytz

# api key (note: with free polygon api-key you only get 2 years of 1-min data)
api_key = 'dwXemOypCihy0ITO00CtgN7uPph406gk'
output_folder = 'historical_data' 

# Make sure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# tickers in a tickers.csv file (Example format: AAPL,TSLA,MSFT)
tickers = pd.read_csv('tickers.csv',header=None).values.tolist()
tickers = tickers[0]

# or it can be a list like this:
#tickers = ['TSLA', 'AAPL', 'NVDA']

# Set start and end dates (without timezone conversion - data'll be in UTC format)
# Note: with paid API key you can replace 2* with whatever years of data you want
start_date = (datetime.now(pytz.UTC) - timedelta(days=2*365)) 
end_date = datetime.now(pytz.UTC).replace(hour=23, minute=59, second=59, microsecond=0)

# or manually put the date
# start_date = datetime.strptime('2022-11-30', "%Y-%m-%d").replace(tzinfo=pytz.UTC)
# end_date = datetime.strptime('2024-11-29', "%Y-%m-%d").replace(tzinfo=pytz.UTC)

# to fetch and save data
def fetch_and_save_data(ticker, start_date, end_date):
    current_start_date = start_date
    file_path = os.path.join(output_folder, f"{ticker}_1_min_data.csv")

    while current_start_date < end_date:
        # Fetch data for each batch up to 50,000 records (it's the limit with free API key)
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/"
            f"{current_start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            f"?adjusted=true&sort=asc&limit=50000&apiKey={api_key}"
        )
        print(f"\nFetching data for {ticker} from {current_start_date} to {end_date}...")

        try:
            response = requests.get(url)
            data = response.json()

            # Check for valid response with results
            if response.status_code == 200 and "results" in data and data["results"]:
                # Create DataFrame from API results
                df = pd.DataFrame(data["results"])
                df['timestamp'] = pd.to_datetime(df['t'], unit='ms') 

                # Convert timestamp to EST (comment this out, if don't want to convert into EST)
                df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')

                # Rename columns to standard format
                df = df.rename(columns={
                    "o": "open", "c": "close", "h": "high",
                    "l": "low", "v": "volume", "vw": "vwap"
                }).drop(columns=["t", "n"])

                # Save data to CSV
                if os.path.exists(file_path):
                    df.to_csv(file_path, mode='a', header=False, index=False)
                else:
                    df.to_csv(file_path, index=False)

                print(f"Saved {len(df)} rows for {ticker}.")

                # Update `current_start_date` based on the last row's timestamp
                last_timestamp = pd.to_datetime(df['timestamp'].iloc[-1])

                print(f"No new data available for {ticker}, stopping. Lat_timestamp = {last_timestamp} and current start date = {current_start_date} --1 ")
                # Break loop if no new data is being fetched
                if last_timestamp.date() == current_start_date.date():
                    print(f"No new data available for {ticker}, stopping. Lat_timestamp = {last_timestamp} and current start date = {current_start_date} --2 ")
                    break

                current_start_date = last_timestamp + timedelta(minutes=1)

                # Back to UTC for next API call (don't have to do this if haven't converted to EST)
                current_start_date = current_start_date.tz_convert('UTC')  

            else:
                print(f"No more data available for {ticker}. Ending fetch loop.")
                break

            # Free API key limit handling (can only make 5 API calls/minute)
            time.sleep(13)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            break

if __name__ == '__main__':
    for ticker in tickers:
        fetch_and_save_data(ticker, start_date, end_date)
        time.sleep(13)
