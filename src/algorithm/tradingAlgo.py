from .tradingAlgoFramework import *
from datetime import datetime
from tools import targetStockTools

def workflow_instance(stock_ticker):
    '''
    This executes the decision-making to buy/sell a stock at the time it is called.

    Arguments:
        stock_ticker (string)
        
    Return:
        1, 0, -1 (int) : bought, nothing, sold
    '''
    # Get Data
    stock_data = fetch_stock_data(stock_ticker,'1h', 100)
    stock_price = stock_data['close']
    # Buy? --> Buy
    if decide_buy(stock_data):
        exec_purchase(stock_ticker, 1, stock_price)
        return -stock_price
    # Sell? --> Sell
    elif decide_sell(stock_data):
        exec_sell(stock_ticker, 1, stock_price)
        return stock_price
    return 0

def loopOverStocks():
    '''
    Distributes workflow_instance over all the stocks you're tracking & keeps records
    '''
    event_log = {"timestamp": str(datetime.now()), "orders": []}
    tickers = targetStockTools.listTickers()
    for stock_ticker in tickers:
        tmp_log = {"name": stock_ticker}
        tmp_log["change"] = workflow_instance(stock_ticker)
        event_log["orders"].append(tmp_log)
    with open("../py_trading/src/data/history.json", "r") as f:
        tmp = json.load(f)
    tmp["log"].append(event_log)
    print(tmp)
    with open("../py_trading/src/data/history.json", "w") as f:
        json.dump(tmp, f)
        