"""
This is the basic structure for the trading algorithm. This creates the environment that manages possessions and transactions. That occurs client-side. 


The API is contained in the function that fetches data. Everything else occus on the machine.
"""
from twelvedata import TDClient
from tools import assetTools as at
from tools import targetStockTools as tst
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
        stock_ticker: ticker 
        interval: time frame (1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month)
        size: the number of data points to retrieve

    Return:
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
    Execute a purchase.

    Argument:
        stock_ticker
        shares: The amount of shares to buy 
        price_per_share: The value of each share
        
    Return:
        success (True) or failure (False)
    """
    value = shares * float(price_per_share)
    funds_usd = at.getAmt('funds_usd')
    if value < funds_usd:
        return False
    # Spend money
    at.updateAssets('funds_usd', -shares*price_per_share)
    # Update possessions
    at.updateAssets(stock_ticker, shares)
    return True

def exec_sell(stock_ticker: str, shares: float, price_per_share: float) -> bool:
    """

    Execute a sell. 
    
    Argument:
        stock_ticker
        shares: The amount of shares to sell 
        price_per_share: The price of each share 

    Return:
        success (True) or failure (False)
    """
    if not at.checkPresence(stock_ticker):
        raise Exception(f"Attempted to sell nonexistent asset: {stock_ticker}.")
    else: 
        # Ensure transaction is valid
        amt = at.getAmt(stock_ticker)
        if shares > amt:
            return False
        # Excecute transaction
        at.updateAssets(stock_ticker, -shares)
        at.updateAssets('funds_usd', shares*price_per_share)
        # Clean list
        at.trashCollector()
    return True 


# Buy/Sell if stock is increasing / decreasing in value 
def decide_buy(stock_data: pd.DataFrame) -> bool:
    """
    Decide whether to buy a stock

    Argument: 
        stock_data : a pandas dataframe of an assets historical prices

    Return:
        choice (True / False)
    """
    # Calculate moving average
    long = stock_data['close'].copy().rolling(100).mean()
    short = stock_data['close'].copy().rolling(50).mean()
    # Get moving average
    long_average = long.iloc[-1]
    short_average = short.iloc[-1]
    # Return true if trending upwards
    # Trending upwards if the short > long 
    return short_average > long_average

def decide_sell(stock_data: pd.DataFrame) -> bool:
    """
    Decide whether to sell a stock

    Argument: 
        stock_data : a pandas dataframe of an assets historical prices

    Return:
        choice (True / False)
    """
    # Calculate moving average
    long = stock_data['close'].copy().rolling(100).mean()
    short = stock_data['close'].copy().rolling(50).mean()
    # Get moving average
    long_average = long.iloc[-1]
    short_average = short.iloc[-1]
    # Return true if trending downwards
    # Trending downwards if the short > long 
    return short_average < long_average
