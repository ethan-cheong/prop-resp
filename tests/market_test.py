import unittest
from root.market import Market
import numpy as np

class BasicInitTests(unittest.TestCase):
    def test(self):
        budget = np.array([1,1,1]) # each player gets 1 money
        utility = np.array([[0.5, 0.7], [2, 4], [1,3]]) # 2 goods
        # 
        bid = np.array([[0.5, 1], [0,1], [0,1]]) # each person bids all their money on good 2
        market1 = Market(budget=budget, start_bids=bid, utility = utility)
        market1.prop_resp_update()
    

if __name__ == '__main__':
    unittest.main()