# Get Historical Data using Polygon.io API

This repository provides a well-organized and efficient way to retrieve various levels of historical data from Polygon.io.

## Key Notes

- Free Polygon.io API keys allow access to up to 2 years of intraday (1-minute) data. Sign up for a free key here: https://polygon.io/dashboard/api-keys
- For more extensive data needs, consider upgrading to a paid Polygon.io plan.
- If you need help getting stock tickers, this GitHub repo may be helpful: https://github.com/shilewenuw/get_all_tickers

## Features

- **Flexible Data Granularity:** This code focuses on intraday (1-minute) data, but you can easily modify the URL to retrieve data with different granularities (e.g., 5 minutes, 15 minutes, or daily). Simply adjust the "1/minute" part in the URL to match your desired timeframe.
- **Efficient Data Retrieval:** The code incorporates a sleep function to circumvent Polygon.io's query limitations. This allows you to retrieve a significant amount of data by strategically pausing between requests.
- **Customizable Timeframe:** You can effortlessly adjust the start and end time parameters within the code to obtain data for your specific timeframe.
- **Ticker Management:** You have two options for providing tickers:
    - Replace the tickers.csv file with the desired tickers, following the format presented in the existing tickers.csv file.
    - Alternatively, define a list of tickers directly within the get_intraday_data.py file.

## Installation

Use the following pip command to install the necessary libraries:

```

pip install ...

```

## Run the script

After installation, simply run the 'get_intraday_data.py' script

```

python get_intraday_data.py

```

## Output

The retrieved data will be saved to the historical_data folder in this format: ticker_1_min_data.csv.
