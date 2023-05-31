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
    assets['list'].append(ticker)
    with open("../py_trading/src/data/targetStock.json", 'w') as f:
        json.dump(assets, f)

def listTickers():
    """
    Returns a list of the tracked tickers
    """
    with open("../py_trading/src/data/targetStock.json", 'r') as f:
        assets = json.load(f)
    return assets['list']

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
    return ticker in assets['list']