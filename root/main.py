from market import Market
import numpy as np

# Initialise a market.

# Initialise starting budgets.

budget = np.array([1,2,3,4]) # 4 individuals

utility = np.array([
    [0,2,5],
    [2,3,4],
    [10,4,5],
    [2, 20, 3]
])

bids = np.array([
    [0,1,0],
    [0,0,2],
    [0,3,0],
    [1,1,1]
])


market = Market(budget=budget, start_bids=bids, utility=utility)
for i in range(5):
    print(market.get_qty())
    market.prop_resp_update()