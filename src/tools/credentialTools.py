"""
Functions to edit API portion of session_data.json
"""
import json


def setToken(token:str) -> bool:
    """
    Set the API token.
    """
    try: 
        with open("../py_trading/src/data/session_data.json", 'r') as f:
            assets = json.load(f)
        assets['sessions'][-1]['API token'] = token
        with open("../py_trading/src/data/session_data.json", 'w') as f:
            json.dump(assets, f)
        return True
    except:
        return False
