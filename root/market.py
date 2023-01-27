import numpy as np
from typing import Callable

class Market:
    """
    Class to represent a market with proportionate response dynamics (or variations)
    Market initialized with n buyers and m goods. 
    Buyers will be indexed with i and goods with j by convention.

    ...

    Attributes
    ----------
    time : int
        current simulation time step, t=0,1,...
    price : np.array
        1d 1xm vector. price[j] gives the price of good j.
    qty : np.array
        2d nxm array. qty[i,j] gives the quantity of good j distributed to buyer i at time t.
    bid : np.array
        2d nxm array. bid[i,j] buyer i's bid for good j at time t.
    budget : np.array
        1d 1xn array. budget[i] gives buyer i's budget.
    utility : np.array
        2d nxm array. utility[i,j] gives the u_ij used in buyer i's utility function.

    Methods
    -------
    step_time():
        Increments time by one step and performs the update rule.
    """

    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array):
        
        self.n_buyers, self.n_goods = utility.shape
        #   TODO: Check that dimensions of inputs conform

        self.time = 0
        self.bid = start_bids
        self.price = np.sum(start_bids, axis=0) # each good's price is the sum of bids
        self.qty = (start_bids.T / self.price[:, None]).T
        self.budget = budget
        self.utility = utility
        # Assume that at time step 0, 

    def get_price():
        return self.price

    def get_qty():
        return self.qty
    
    def get_bid():
        return self.bid
    
    