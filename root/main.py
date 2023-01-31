from market import Market
import numpy as np
from initializer import Initializer

# Initialise a market.
initializer = Initializer(50, 1000, 1)
params = initializer.initialize_linear_utilities_basic()
#print(params)
print(params[0].shape) # budget
print(params[1].shape) # bids
print(params[2].shape) # utils

market = Market(params[0], params[1], params[2])
# print(params[0])
# print(params[1])
# print(np.sum(params[1], axis=1))

for i in range(1000):
    print(market.get_qty())
    market.prop_resp_update()