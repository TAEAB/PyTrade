from .tradingAlgoFramework import *
from datetime import datetime
import tools.targetStockTools as tst
import tools. historyTools as ht

def workflow_instance(stock_ticker: str) -> float:
    '''
    This executes the decision-making to buy/sell a stock at the time it is called.

    Arguments:
        stock_ticker (string)
        
    Return:
        change (float): change in funds
    '''
    # Get Data
    stock_data = fetch_stock_data(stock_ticker,'1h', 100)
    stock_price = stock_data['close']
    # Buy? --> Buy
    if decide_buy(stock_ticker, stock_data):
        exec_purchase(stock_ticker, 1, stock_price)
        return -stock_price
    # Sell? --> Sell
    elif decide_sell(stock_ticker, stock_data):
        exec_sell(stock_ticker, 1, stock_price)
        return stock_price
    return 0

def loopOverStocks() -> None:
    '''
    Distributes workflow_instance over all tracked stocks
    '''
    tickers = tst.listTickers()
    events = []
    for stock_ticker in tickers:
        events.append(
            ht.logEvent(stock_ticker, 
                        workflow_instance(stock_ticker))
        )
    ht.logEvents(events)
        