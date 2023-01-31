import numpy as np

class Initializer:
    """
    Class to initialize variables for dynamics.

    Attributes
    ----------
    n_goods : int
        Number of goods in the market. 
    n_buyers : int
        Number of buyers in the market.
    seed : int
        Number for random number generation

    Methods
    -------
    get_n_goods():
        returns the number of goods.
    get_n_buyers():
        returns the number of buyers.
    """
    def __init__(self, n_goods: int, n_buyers: int, seed: int):
        if (n_goods <= 0 or n_buyers <= 0):
            raise ValueError("Must have more than 0 buyers and goods.")
        self.n_goods = n_goods
        self.n_buyers = n_buyers
        self.seed = seed
    
    def initialize_linear_utilities_basic(self):
        util = np.random.rand(self.n_buyers, self.n_goods)
        # utilities are sampled from Unif[0,1]
        
        # normalize utilities to 1. In line with Zhang's convergence proof
        util_row_sums = util.sum(axis=1)
        util = util / util_row_sums[:, np.newaxis]
        
        # budgets sum to 1 - again in line with zhang's convergence proof

        budget = np.ones(self.n_buyers)

        # bids - initialise start bid as the amount of utility they get from the good?
        # bids - rescale utilities to sum to budget per good.
        # multiply by 1.01 for easy fix for loss of precision for floats
        bids = (util.T/(1.01*util.sum(axis=1))).T

        return [budget, bids, util]
        # TODO: choose how you wanna initialize start bids
        # TODO: Dealing with the rounding to 0 problem.

    
        


