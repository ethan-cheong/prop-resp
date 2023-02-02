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

        #bids = np.full((self.n_buyers, self.n_goods), 1/self.n_goods)
        
        return [budget, bids, util]

    def initialize_linear_utilities_discrete(self, high=2):
        """
        Initializes util weights having value 0/1 with 50% probability each. Then normalize utilities to 1.

        Params
        ------
        high : int
            Upper bound (exclusive) for integer utility weights. Default initializes utility weights of either 0 or 1.
        
        """
        util = np.random.randint(0, high, size=(self.n_buyers, self.n_goods))
        util_row_sums = util.sum(axis=1)
        for i in range(len(util_row_sums)):
            if util_row_sums[i]==0:
                index = np.random.randint(0, len(util[i]))
                util[i, index] = 1
            util_row_sums[i] = 1
        util = util / util_row_sums[:, np.newaxis]
        
        # budgets sum to 1 - again in line with zhang's convergence proof

        budget = np.ones(self.n_buyers)

        # bids - initialise start bid as the amount of utility they get from the good?
        # bids - rescale utilities to sum to budget per good.
        # multiply by 1.01 for easy fix for loss of precision for floats
        bids = (util.T/(1.01*util.sum(axis=1))).T
        # TODO: Deal with the rounding to 0 error
        return [budget, bids, util]
        
    # TODO: more complicated utility initializations!

    
        


