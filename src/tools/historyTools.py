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
    events_log = {"timestamp": str(datetime.now()), }
    for event in events:
        ticker = event["ticker"]
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
    event_log = {"asset": ticker, "delta_value_held": delta_value_held}
    return event_log

def getHistory() -> pd.DataFrame:
    """
    Returns the entire history as a pandas dataframe
    """
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    hist = pd.DataFrame(tmp["log"])
    return hist

def resetHistory() -> None: 
    """
    Clears all data from the history log
    """
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    tmp["log"] = []
    with open("../py_trading/src/data/history.json", "w") as f:
        json.dump(tmp, f)

## TODO: Develop accessor for specific assets / debug

if __name__ == "__main__":
    hist = getHistory()
    print(hist)




