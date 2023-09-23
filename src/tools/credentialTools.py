"""
Scripts to edit twelveDataAPI.json
"""
import json


def setToken(token:str) -> bool:
    """
    Set the API token.
    """
    try: 
        with open("../py_trading/src/data/twelveDataAPI.json", 'r') as f:
            assets = json.load(f)
        assets['token'] = token
        with open("../py_trading/src/data/twelveDataAPI.json", 'w') as f:
            json.dump(assets, f)
        return True
    except:
        return False
