"""
Scripts to edit targetStock.json
"""

import json

def addTicker(ticker:str) -> None:
    """
    Adds a stock to the list of tracked assets
    """
    with open("../py_trading/src/data/session_data.json", 'r') as f:
        assets = json.load(f)
    new_target = {
                    "ticker": ticker,
                }
    assets['sessions'][-1]['target stock'].append(new_target)
    with open("../py_trading/src/data/session_data.json", 'w') as f:
        json.dump(assets, f)

def listTickers() -> list:
    """
    Returns a list of the tracked tickers
    """
    with open("../py_trading/src/data/session_data.json", 'r') as f:
        assets = json.load(f)
    return [x["ticker"] for x in assets['sessions'][-1]['target stock']]

# Might be irrelevant as new sessions are created 
def resetTickers() -> None:
    """
    Clears list of tickers
    """
    with open("../py_trading/src/data/session_data.json", 'r') as f:
        sessions = json.load(f)
    sessions['sessions'][-1]["target stock"] = []
    with open("../py_trading/src/data/session_data.json", 'w') as f:
        json.dump(sessions, f)

def checkTickers(ticker:str) -> bool:
    """
    Checks whether ticker is tracked in list
    """
    with open("../py_trading/src/data/session_data.json", 'r') as f:
        sessions = json.load(f)
    return ticker in sessions['sessions'][-1]['target stock']

