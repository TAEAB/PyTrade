'''
This initializes the assets.json file.
'''
import json

def initializeFunds(funds_usd:float) -> bool:
    '''
    Set all assets to initial values

    Arguments:
        funds_usd: The initial funds in dollars
    
    Return:
        success (True) or failure (False)
    '''
    hardSet('funds_usd', 0)
    updateAssets('funds_usd', funds_usd)

def updateAssets(key:str, amt:float) -> bool:
    '''
    Arguments:
        key (string): label of the asset
        amt (float): the change in amount of the asset
        
    Return:
        success (True) or failure (False)
    '''
    try: 
        with open("../py_trading/src/data/assets.json", 'r') as assets_json:
            assets = json.load(assets_json)
        # either initialize the json entry or add to its value
        if key in assets:
            assets[key] += amt
        if key not in assets:
            assets[key] = amt
        with open('../py_trading/src/data/assets.json', 'w') as assets_json:
            json.dump(assets, assets_json)
        return True
    except: 
        return False

def trashCollector() -> bool:
    """
    Remove any entries in the stock portion of the JSON with a zero value.
    """
    try:
        with open("../py_trading/src/data/assets.json", 'r') as assets_json:
            assets = json.load(assets_json)
        zero_keys = {key for key in assets if assets[key][0] == 0}
        for key in zero_keys:
            del assets[key]
        with open('../py_trading/src/data/assets.json', 'w') as assets_json:
            json.dump(assets, assets_json)
        return True
    except:
        return False
    
def checkPresence(key:str) -> bool:
    """
    Check whether the key is in the JSON file.
    """
    with open("../py_trading/src/data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    return key in assets

def getAmt(key:str) -> float:
    """
    Access amount of an asset in the JSON.
    """
    with open("../py_trading/src/data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    if key not in assets:
        raise Exception("Target asset not in possesions")
    return assets[key]

def hardSet(key:str, amt:float) -> bool:
    '''
    Set the value of an asset in the JSON.
    
    Arguments:
        key: label of the asset
        amt: new amount of asset
    
    Return:
        success (True) or failure (False)
    '''
    try: 
        with open("../py_trading/src/data/assets.json", 'r') as assets_json:
            assets = json.load(assets_json)
        assets[key] = amt
        with open("../py_trading/src/data/assets.json", 'w') as assets_json:
            json.dump(assets, assets_json)
        return True
    except:
        return False
    
if __name__ == "__main__":
    initializeFunds(10)
    updateAssets("aapl", 23)
