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
        budget = np.ones(self.n_buyers)
        # bids - initialise start bid as the amount of utility they get from the good?
        # bids - rescale utilities to sum to budget per good.
        # TODO: Easy fix for loss of precision problem
        bids = (util.T/(1.1*util.sum(axis=1))).T
        return [budget, bids, util]
        # TODO: choose how you wanna initialize start bids
        


