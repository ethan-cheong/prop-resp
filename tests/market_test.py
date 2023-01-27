import unittest
from root.market import Market
import numpy as np

class BasicInitTests(unittest.TestCase):
    def test(self):
        budget = np.array([1.5,1,1]) # each player gets 1 money
        utility = np.array([[0.5, 0.7], [2, 4], [1,3]]) # 2 goods
        # 
        bid = np.array([[0.5, 1], [0,1], [0,1]]) # each person bids all their money on good 2
        market1 = Market(budget=budget, start_bids=bid, utility = utility)
        market1.prop_resp_update()

class PropRespBasicTest1(unittest.TestCase):
    def test(self):
        budget = np.array([1,2,3,4]) # 4 individuals

        utility = np.array([
            [0,2,5],
            [2,3,4],
            [10,4,5],
            [2, 20, 3]
        ])

        bids = np.array([
            [0,1,0], # [1,0,0] makes an error
            [0,0,1],
            [0,1,0],
            [1,0,0]
        ])


        market = Market(budget=budget, start_bids=bids, utility=utility)
        for i in range(5):
            print(market.get_qty())
            market.prop_resp_update() # this creates an error because initial bids are INCONSISTENT with valuation.
            # basically, if someone values

class PropRespBasicTest2(unittest.TestCase):
    def test(self):
        # TODO: work through this example on paper
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
            [1,1,2]
        ])


        market = Market(budget=budget, start_bids=bids, utility=utility)
        for i in range(5):
            print("Loop iteration " + str(i))
            market.prop_resp_update() 


if __name__ == '__main__':
    unittest.main()