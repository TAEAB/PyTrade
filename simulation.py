'''
This is a simulation testing whether the moving average trading heuristic is profitable
'''


import pandas as pd
import random
import matplotlib.pyplot as plt

# Decision mechanics

def decide_buy(series: pd.DataFrame) -> bool:
    return short_average(series) > long_average(series)

def decide_sell(series: pd.DataFrame) -> bool:
    return short_average(series) < long_average(series)

def long_average(series: pd.DataFrame) -> float:
    raw = series.copy().rolling(5).mean()
    return raw.iloc[-1].values[0]

def short_average(series: pd.DataFrame) -> float:
    raw = series.copy().rolling(3).mean()
    return raw.iloc[-1].values[0]


# Price series
ls = [random.randint(50, 150) for i in range(105)]
prices = pd.DataFrame(ls)


# Initialize variables 
funds = 500
shares = 0 


# Simulation

# This will track the breakdown of my assets
log = []

for i in range(100):
    i+=5
    price = prices.iloc[i].values[0]
    if decide_buy(prices[i-5:i]) and funds > price:
        funds -= price
        shares += 1
    elif decide_sell(prices[i-5:i]) and shares > 0:
        funds += price
        shares -= 1
    log.append({
        "index": i,
        "balance": funds + shares*price,
        "funds": funds,
        "stock": shares*price,
        "net change": funds + shares*price - 500,
    })

# Final tally
print(f"Final balance: ${funds + shares * prices.iloc[-1].values[0]}")
print(f"Uninvested cash: ${funds}")
print(f"{shares} shares @ ${prices.iloc[-1].values[0]} = ${shares * prices.iloc[-1].values[0]} in stock")

# Graph performance
performance = pd.DataFrame(log)
performance.plot(subplots=True, grid=True)
plt.show()

