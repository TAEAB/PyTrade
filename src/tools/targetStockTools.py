"""
Scripts to edit targetStock.json
"""

import json

def addTicker(ticker:str) -> None:
    """
    Adds a stock to the list of tracked assets
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    new_target = {
                    "ticker": ticker,
                    "long_is_above_short": False # False by default--requires initialization
                }
    assets['list'].append(new_target)
    with open("../py_trading/src/data/targetStock.json", 'w') as f:
        json.dump(assets, f)

def listTickers() -> list:
    """
    Returns a list of the tracked tickers
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return [x["ticker"] for x in assets['list']]

def resetTickers() -> None:
    """
    Clears list of tickers
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    assets['list'] = []
    with open("../py_trading/src/data/targetStock.json", 'w') as f:
        json.dump(assets, f)

def checkTickers(ticker:str) -> bool:
    """
    Checks whether ticker is tracked in list
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return ticker in [x["ticker"] for x in assets['list']]


# This can be slow for large lists of tracked assets due to linear filtering
# Unique to moving-average approach / not necessary for other trading heuristics
def getRelativeAveragePosition(ticker: str) -> bool:
    """
    Returns true if 100 day average is greater than 50 day average. False otherwise.
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return list(filter(lambda x : x["ticker"] == ticker , assets["list"]))[0]["long_is_above_short"]