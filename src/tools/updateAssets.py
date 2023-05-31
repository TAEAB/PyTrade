'''
This initializes the assets.json file.
'''
import json

def initializeFunds(funds_usd):
    '''
    Set all assets to initial values

    Arguments:
        funds_usd (float): The initial funds in dollars
    
    Return:
        (boolean): success or failure
    '''
    hardSet('funds_usd', 0)
    updateAssets('funds_usd', funds_usd)

def updateAssets(key, amt):
    '''
    Arguments:
        key (string): label of the asset
        amt (float): the change in amount of the asset
        val (float): the changes in value of the asset
        
    Return:
        (boolean): success or failure
    '''
    with open("../data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    # either initialize the json entry or add to its value
    if key in assets:
        assets[key] += amt
    if key not in assets:
        assets[key] = amt
    with open('../data/assets.json', 'w') as assets_json:
        json.dump(assets, assets_json)
    return True

def trashCollector():
    """
    Remove any entries in the stock portion of the JSON with a zero value.
    """
    with open("../data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    zero_keys = {key for key in assets if assets[key][0] == 0}
    for key in zero_keys:
        del assets[key]
    with open('../data/assets.json', 'w') as assets_json:
        json.dump(assets, assets_json)
    return True

def checkPresence(key):
    """
    Check whether the key is in the JSON file.
    """
    with open("../data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    return key in assets

def getAmt(key):
    """
    Access amount of an asset in the JSON.
    """
    with open("../data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    if key not in assets:
        raise Exception("Target asset not in possesions")
    return assets[key]

def hardSet(key, amt):
    '''
    Set the value of an asset in the JSON.
    
    Arguments:
        key (string): label of the asset
        amt (float): new amount of asset
    
    Return:
        (boolean): success or failure
    '''
    with open("../data/assets.json", 'r') as assets_json:
        assets = json.load(assets_json)
    assets[key] = amt
    with open('../data/assets.json', 'w') as assets_json:
        json.dump(assets, assets_json)
        
if __name__ == "__main__":
    initializeFunds(10)
    updateAssets("aaple", 23)
