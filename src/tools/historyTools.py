"""
Functions to edit history.json
"""
import json
import pandas as pd
from datetime import datetime
import time

def logEvents(events: list) -> None:
    """
    Makes a single entry for all events from given time in the history JSON
    """
    if type(events) != str:
        raise TypeError(f"parameter 'events' expects list, got {type(events)}")
    events_log = {"timestamp": str(datetime.now()), }
    for event in events:
        ticker = event["asset"]
        delta_value_held = event["delta_value_held"]
        events_log[ticker] = delta_value_held
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    tmp["log"].append(events_log)
    with open("../py_trading/src/data/history.json", "w") as f:
        json.dump(tmp, f)
        
def logEvent(ticker: str, delta_value_held: float) -> dict:
    """
    Record the change in a stock at a given time in the history JSON
    
    Return: 
        event_log: dict summarizing change in asset
    """
    if type(ticker) != str:
        raise TypeError(f"parameter 'ticker' expects string, got {type(ticker)}")
    if type(delta_value_held) != float:
        raise TypeError(f"parameter 'delta_value_held' expects float, got {type(delta_value_held)}")
    
    event_log = {"asset": ticker, "delta_value_held": delta_value_held}
    return event_log

def getHistory(asset:str = None) -> pd.DataFrame:
    """
    Returns the history as a pandas dataframe. Either for a given asset, or for all if none requested.
    """
    tmp = pd.read_json("../py_trading/src/data/history.json")
    hist = pd.DataFrame.from_records(tmp["log"]).set_index('timestamp')
    if asset == None:
        return hist
    if type(asset) == str: 
        if asset not in hist:
            raise KeyError(asset)
        return hist[asset]
    elif type(asset) != str:
        raise TypeError("asset: Expected string")

def resetHistory() -> None: 
    """
    Clears all data from the history log
    """
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    tmp["log"] = []
    with open("../py_trading/src/data/history.json", "w") as f:
        json.dump(tmp, f)
