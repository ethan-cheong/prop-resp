import numpy as np

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
        if len(budget) != self.n_buyers:
            raise ValueError("Check that budget and utility dimensions conform. Budget should be 1xn and Utility should be mxn")
        if start_bids.shape != utility.shape:
            raise ValueError("Check that starting bids and utility have the same dimensions.")
        
        if any(np.sum(start_bids, axis=1) > budget):
            raise ValueError("Starting bids of each invididual cannot be greater than their budget!")

        self.time = 0
        self.bid = start_bids
        self.price = np.sum(start_bids, axis=0) # each good's price is the sum of bids
        #   TODO: Throw an error if goods start off with 0 price.
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good has reached 0.")
        
        self.qty = (start_bids.T / self.price[:, None]).T
        self.budget = budget
        self.utility = utility
        # Assume that at time step 0, 

    def get_price(self):
        return self.price

    def get_qty(self):
        return self.qty
    
    def get_bid(self):
        return self.bid

    def prop_resp_update(self):
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now

        # TODO: Practical Proportional Response.
        # Problem: Each time step is very slow!! how to fix?
        for i in range(self.n_buyers):
            sum_utility = 0
            for k in range(self.n_goods):
                sum_utility += self.utility[i, k] * self.qty[i, k]
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")
                    # TODO: Prove that we only get a division by 0 error if initial bids are inconsistent with utilities. 
                    # TODO: You can put this in the diss / notes to laszlo. AKA, they put all their money into a good they get no money for.

            for j in range(self.n_goods):
                self.bid[i, j] = self.budget[i] * self.utility[i, j] * self.qty[i, j] / sum_utility
        
        self.time += 1
    
    