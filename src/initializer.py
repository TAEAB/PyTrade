"""
Used to set up:

 - Starting Funds
 - Tracked Assets
 - API Credentials

"""

import tools.targetStockTools as tst
import tools.assetTools as at
import tools.credentialTools as ct

import algorithm.tradingAlgoFramework as taf

if __name__ == "__main__":
    # Prepare API
    ct.setToken(str(input("Copy the API token: ")))
    # Set up tracking list
    tst.resetTickers()
    raw_tracking_list = input("Please list the symbols for the stocks of interest, separated by commas: ")
    tracking_list = [x.strip() for x in raw_tracking_list.split(",")]
    for ticker in tracking_list:
        tst.addTicker(ticker)
    # (Tracking List) Initialize long_is_above_short values
    for ticker in tracking_list:
        stock_data = taf.fetch_stock_data(ticker, "1h", 100)
        long = stock_data['close'].copy().rolling(100).mean()
        short = stock_data['close'].copy().rolling(50).mean()    
        long_is_above_short = long > short
    # Initialize Funds
    at.initializeFunds(float(input("Input the initial funds as a float: ")))
    # Reset History
    # TODO



