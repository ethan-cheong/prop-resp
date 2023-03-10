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
        # Don't separate the bidding from utilities.
        # bids - initialise start bid as the amount of utility they get from the good?
        # bids - rescale utilities to sum to budget per good.
        # multiply by 1.01 for easy fix for loss of precision for floats
        bids = (util.T/(1.01*util.sum(axis=1))).T
        return [budget, bids, util]

    def initialize_low_mid_high_utilities(self, n_goods): 
        """
        Initializes utilities for certain individuals having preferences for certain goods.
        Good's preferences are randomly distributed among groups of individuals.


         
        """

    def initialize_preferred_goods_manual(self, input, noise):
        # TODO: Fix this later by adding in automatic generation
        # Idea: add in discrete combinations of utilities, shuffle them for each individual, add in random noise
        """
        Adds random noise to matrix of utilities.
        Params
        ------
        input: np.array
            nxm array of utilities
        noise: float
            non-negative standard deviation of gaussian noise
        """
        noise_array = np.random.normal(1.0, noise, size=input.shape)
        budget = np.ones(input.shape[0])
        util = input * noise_array
        #bids = (util.T/(1.01*util.sum(axis=1))).T
        # constant bids below
        bids = np.full(shape = input.shape, fill_value = 1 / input.shape[1])
        return [budget, bids, util]
        

    # TODO: more complicated utility initializations, like below
    # 1. Randomly assign agents to groups, with different distributions (liking a good more or less)
    # 2. Giving goods different values
    # 3. Randomly knock out utilities for some of the goods.

    
        


