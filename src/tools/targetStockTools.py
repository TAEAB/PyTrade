"""
Scripts to edit targetStock.json
"""

import json

def addTicker(ticker:str):
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

def listTickers():
    """
    Returns a list of the tracked tickers
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return [x["ticker"] for x in assets['list']]

def resetTickers():
    """
    Clears list of tickers
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    assets['list'] = []
    with open("../py_trading/src/data/targetStock.json", 'w') as f:
        json.dump(assets, f)

def checkTickers(ticker:str):
    """
    Checks whether ticker is tracked in list
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return ticker in [x["ticker"] for x in assets['list']]