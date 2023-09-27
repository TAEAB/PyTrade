"""
Functions to edit history.json
"""
import json
import pandas as pd
from datetime import datetime


def logEvents(events: list) -> None:
    """
    Makes a single entry for all events from given time in the history JSON
    """
    events_log = {"timestamp": str(datetime.now()), "events": []}
    for event in events:
        events_log["events"].append(event)
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    tmp["log"].append(events_log)
    with open("../py_trading/src/data/history.json", "w") as f:
        json.dump(tmp, f)
        
def logEvent(ticker: str, change_in_held_value: float) -> dict:
    """
    Record the change in a stock at a given time in the history JSON
    
    Return: 
        event_log: dict summarizing change in asset
    """
    event_log = {"asset": ticker, "delta_value_held": change_in_held_value}
    return event_log

def getHistory() -> pd.DataFrame:
    """
    Returns the entire history as a pandas dataframe
    """
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    hist = pd.DataFrame(tmp["log"])
    return hist