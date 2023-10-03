"""
Functions to edit the trading strategy portion of session_data.json
"""
import json


def setPath(path:str) -> bool:
    """
    Set the path to the trading strategies.
    """
    try: 
        with open("../py_trading/src/data/session_data.json", 'r') as f:
            assets = json.load(f)
        assets['sessions'][-1]['strategy path'] = path
        with open("../py_trading/src/data/session_data.json", 'w') as f:
            json.dump(assets, f)
        return True
    except:
        return False
