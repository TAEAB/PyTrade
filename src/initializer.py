"""
Used to set up:

 - Starting Funds
 - Tracked Assets
 - API Credentials

"""
import json

import tools.targetStockTools as tst
import tools.assetTools as at
import tools.credentialTools as ct
import tools.historyTools as ht
import tools.strategyTools as st

import algorithm.tradingAlgoFramework as taf

if __name__ == "__main__":
    # TODO : Add request for path to trading strategy file
    # Request Path to trading strategy file
    st.setPath(str(input("Path to strategy scripts: ")))
    # Prepare API
    ct.setToken(str(input("API token: ")))
    # Set up tracking list
    tst.resetTickers()
    raw_tracking_list = input("Please list the symbols for the stocks of interest, separated by commas: ")
    tracking_list = [x.strip() for x in raw_tracking_list.split(",")]
    for ticker in tracking_list:
        tst.addTicker(ticker)
    # Initialize Funds
    init_funds = float(input("Input the initial funds as a float: "))
    with open("../py_trading/src/data/session_data.json", "r") as f:
        session_data = json.load(f)
    with open("../py_trading/src/data/session_data.json", "w") as f:
        json.dump(at.updateAssets("initial_funds", init_funds, session_data), f)
    with open("../py_trading/src/data/assets.json", "r") as g:
        asset_data = json.load(g)
    with open("../py_trading/src/data/assets.json", "w") as f:
        json.dump(at.initializeFunds(init_funds, asset_data), f)
    # Reset History
    ht.resetHistory()
    



