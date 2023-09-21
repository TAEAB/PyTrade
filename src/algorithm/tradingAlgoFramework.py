"""
This is the basic structure for the trading algorithm. This creates the environment that manages possessions and transactions. That occurs client-side. 


The API is contained in the function that fetches data. Everything else occus on the machine.
"""
from twelvedata import TDClient
from tools import updateAssets
import json
import pandas as pd

# Initialize the API
import os 
script_dir = os.path.dirname(__file__)
rel_path = os.path.join(script_dir, "../data/TwelveDataAPI.json")
f = open(rel_path)
APIToken = json.load(f)
td = TDClient(apikey=APIToken["token"])

# Bridge to the stock market.
def fetch_stock_data(stock_ticker: str, interval: str, size: int) -> pd.DataFrame:
    """
    Gets the necessary data from the API as a PANDAS dataframe.

    Argument:
        stock_ticker (string): ticker 
        interval (string): time frame (1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month)
        size (int): the number of data points to retrieve

    Return (pd.DataFrame):
        price per share at time of call
    """
    # Construct the time series
    ts = td.time_series(
        symbol=stock_ticker,
        interval=interval,
        timezone="America/New_York",
        outputsize=size
    ).as_pandas()
    return ts


# Keep count of assets
def exec_purchase(stock_ticker: str, shares: float, price_per_share: float) -> bool:
    """
    Execute a purchase through the API.

    Argument:
        stock_ticker (string)
        shares (float): The amount of shares to buy 
        price_per_share (float): The value of each share
        
    Return:
        (boolean)
    """
    value = shares * float(price_per_share)
    funds_usd = updateAssets.getAmt('funds_usd')
    if value < funds_usd:
        raise Exception(f"Purchase (${value}) exceeds available funds (${funds_usd}).")
    # Spend money
    updateAssets('funds_usd', -shares*price_per_share)
    # Update possessions
    updateAssets(stock_ticker, shares)
    return True

def exec_sell(stock_ticker: str, shares: float, price_per_share: float) -> bool:
    """
    Sell shares through the API.

    Argument:
        stock_ticker (string)
        shares (float): The amount of shares to sell 
        price_per_share (float): The price of each share 

    Return:
        (boolean): success or failure
    """
    if not updateAssets.checkPresence(stock_ticker):
        raise Exception(f"Attempted to sell nonexistent asset: {stock_ticker}.")
    else: 
        # Ensure transaction is valid
        amt = updateAssets(stock_ticker)
        if shares > amt:
            raise Exception(f"Attempted to sell more shares than owned: {shares} > {amt}")
        # Excecute transaction
        updateAssets(stock_ticker, -shares)
        updateAssets('funds_usd', shares*price_per_share)
        # Clean list
        updateAssets.trashCollector()
    return True 


# Buy/Sell if stock is increasing / decreasing in value 
def decide_buy(stock_data: pd.DataFrame) -> bool:
    """
    Decide whether to buy a stock

    Argument: 
        stock_data (pandas df): Stock data for past 100 days
    Return:
        choice (boolean)
    """
    # Calculate moving average
    long = stock_data['close'].copy().rolling(100).mean()
    short = stock_data['close'].copy().rolling(50).mean()
    # Get moving average
    long_average = long[long.notnull()].iloc[-1]
    short_average = short[short.notnull()].iloc[-1]
    # Trending upwards if the short > long 
    # Return true if trending upwards and this instance is a change in the trend
    # It is a change in the trend if previously, the long MA was greater than the short MA
    return short_average > long_average and abs(short - long) < 1

def decide_sell(stock_data: pd.DataFrame) -> bool:
    """
    Decide whether to sell a stock

    Argument: 
        stock_data (pandas df)

    Return:
        choice (boolean)
    """
    long = stock_data['close'].copy().ewm(span=100).mean()
    short = stock_data['close'].copy().ewm(span=50).mean()
    return short[0] < long[0] and abs(short - long) < 1

