import numpy as np
from abc import ABC, abstractmethod

class Market:
    """
    Class to represent a market 
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
    individual_utility : np.array
        1d 1xn array. individual_utility[i] gives total utility of buyer i.

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
        self.individual_utility = np.zeros(self.n_buyers)
        # Assume that at time step 0, 

    def get_price(self):
        return self.price

    def get_qty(self):
        return self.qty
    
    def get_bid(self):
        return self.bid

    def get_time(self):
        return self.time 
    
    def get_individual_utility(self):
        return self.individual_utility

    @abstractmethod
    def update(self):
        pass

class PropRespLinearMarket(Market):
    """
    Class to represent a market, using proportionate response dynamics.
    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array):
        super().__init__(budget, start_bids, utility)

    def update(self):
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now
        # Problem: Each time step is very slow!! how to fix?
        for i in range(self.n_buyers):
            # vectorised sum
            sum_utility = np.inner(self.utility[i], self.qty[i])

            self.individual_utility[i] = sum_utility
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")
                   
            for j in range(self.n_goods):
                self.bid[i, j] = self.budget[i] * self.utility[i, j] * self.qty[i, j] / sum_utility
        
        self.time += 1

class GeneralPropRespCDMarket(Market):
    """
    Class to represent a market with Cobb-Douglas Preferences, using general proportionate response dynamics.
    In the CD Market, utility[i,j] is interpreted as the power of good j in buyer i's utility function.
    These sum to 1, as per the standard definition of CD preferences.

    Should converge at the same linear rate, as linear utilities.
    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array):
        super().__init__(budget, start_bids, utility)

    def update(self):
        # COBB DOUGLAS RESOLVES IN ONE STEP.
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now


        for i in range(self.n_buyers):
            # Calculate gradient vector for individual
            gradient = np.zeros(self.n_goods) 
            for j in range(self.n_goods):
                # feature of cobb douglas! 
                if self.qty[i,j]==0:
                    gradient[j] = 0
                else:
                    #gradient[j] = self.utility[i, j]
                    gradient[j] = np.prod(np.power(self.qty[i], self.utility[i]))*  self.qty[i,j]** -1 * (self.utility[i,j])

            sum_utility = np.inner(self.qty[i], gradient) 
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            for j in range(self.n_goods):
                self.bid[i, j] = self.budget[i] * self.qty[i, j] * gradient[j]/ sum_utility
        
        self.time += 1 
    
class GeneralPropRespQLMarketU(Market):
    """
    Class to represent a market with Quasi-Linear Preferences, using general proportionate response dynamics.
    Preferences are of the form u_i = u_i0x_i0 + \sum_{j\ge 1}(u_ijx_ij)^\alpha
    We assume that good 0 corresponds to the linear good.
    Should converge at the same linear rate, as linear utilities.
    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array, alpha: float):
        super().__init__(budget, start_bids, utility)
        self.alpha = alpha;

    def update(self):
     
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now
        
        for i in range(self.n_buyers):
            sum_utility = 0
            sum_utility += self.utility[i,0] * self.qty[i,0]
            for j in range(1, self.n_goods):
                    sum_utility += (self.utility[i, j] * self.qty[i,j]) ** self.alpha
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            self.bid[i, 0] = self.budget[i] * self.qty[i, 0] * self.utility[i,0] / sum_utility

            for j in range(1, self.n_goods):
                self.bid[i, j] = (self.budget[i] * (self.qty[i, j] * self.utility[i,j]) ** self.alpha) / sum_utility
        
        self.time += 1

class GeneralPropRespQLMarketPD(Market):
    """
    Class to represent a market with Quasi-Linear Preferences, using general proportionate response dynamics.
    Preferences are of the form u_i = u_i0x_i0 + \sum_{j\ge 1}(u_ijx_ij)^\alpha
    We assume that good 0 corresponds to the linear good.
    Should converge at the same linear rate, as linear utilities.
    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array, alpha: float):
        super().__init__(budget, start_bids, utility)
        self.alpha = alpha;

    def update(self):
        # Gradient method resolves in one step as well ..
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now
        
        for i in range(self.n_buyers):
            # Calculate gradient vector for individual
            gradient = np.zeros(self.n_goods) 
            gradient[0] = self.utility[i, 0] # gradient for the first good is always constant
            # TODO: Try setting all values to 1 as well
            for j in range(1, self.n_goods):
                if self.qty[i,j]==0:
                    gradient[j] = 0
                else:
                    #gradient[j] = self.utility[i, j]
                    gradient[j] = self.alpha * (self.utility[i,j]) ** self.alpha * self.qty[i,j] ** (self.alpha-1)
            sum_utility = np.inner(self.qty[i], gradient) 
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            for j in range(self.n_goods):
                self.bid[i, j] = self.budget[i] * self.qty[i, j] * gradient[j]/ sum_utility
        
        self.time += 1 

class PropRespZhangMarket(Market):
    """
    Class to represent a market with Zhang's CES preferences, using the proportional response dynamic detailed in his paper.

    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array, alpha: float):
        super().__init__(budget, start_bids, utility)
        self.alpha = alpha;

    def update(self):
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities

        for i in range(self.n_buyers):
            # Calculate gradient vector for individua
            sum_utility = 0
            for j in range(self.n_goods):
                    sum_utility += (self.utility[i, j] * self.qty[i,j]) ** self.alpha
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            for j in range(self.n_goods):
                self.bid[i, j] = (self.budget[i] * (self.qty[i, j] * self.utility[i,j]) ** self.alpha) / sum_utility
        
        self.time += 1

class PropRespZhangMarketSingleLinearBuyer(Market):
    """
    Class to represent a market with Zhang's CES preferences, with a single buyer having linear preferences, using the proportional response dynamic detailed in his paper.

    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array, alpha: float):
        super().__init__(budget, start_bids, utility)
        self.alpha = alpha;

    def update(self):
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities

        for i in range(self.n_buyers):
            # Calculate gradient vector for individua
            sum_utility = 0
            for j in range(self.n_goods):
                    if i==0:
                         sum_utility += (self.utility[i, j] * self.qty[i,j])
                    else:
                         sum_utility += (self.utility[i, j] * self.qty[i,j]) ** self.alpha
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            for j in range(self.n_goods):
                if i==0:
                    self.bid[i, j] = (self.budget[i] * (self.qty[i, j] * self.utility[i,j]) ) / sum_utility 
                else:
                    self.bid[i, j] = (self.budget[i] * (self.qty[i, j] * self.utility[i,j]) ** self.alpha) / sum_utility
        
        self.time += 1

class PropRespQLGroupedMarket(Market):
    """
    Class to represent a market with Quasi-Linear Preferences, using general proportionate response dynamics.
    We have groups A and B goods; A are linear, B are not.
    Preferences are of the form u_i = \sum_{j\in A} u_ijx_ij + \sum_{j\in B}(u_ijx_ij)^\alpha
    We assume that good 0 corresponds to the linear good.
    Should converge at the same linear rate, as linear utilities.
    """
    def __init__(self, budget: np.array, start_bids: np.array, utility: np.array, alpha: float, n_linear):
        super().__init__(budget, start_bids, utility)
        self.alpha = alpha;
        self.n_linear = n_linear # the first n_linear goods will be linear.

    def update(self):
        # Gradient method resolves in one step as well ..
        self.price = np.sum(self.bid, axis=0) # calculate new prices
        if not np.all(self.price):
            raise ZeroDivisionError("Price of good " + str(np.argwhere(self.price == 0)[0]) + " reached 0 at time " + str(self.time) + ".") 
        self.qty = (self.bid.T / self.price[:, None]).T # calculate new quantities
        
        # Update bids. Using for loop for now
        
        for i in range(self.n_buyers):
            # Calculate gradient vector for individual
            sum_utility = 0
            for j in range(self.n_goods):
                if j < self.n_linear:
                    sum_utility += (self.utility[i, j] * self.qty[i,j])
                else:   
                    sum_utility += (self.utility[i, j] * self.qty[i,j]) ** self.alpha
            if sum_utility == 0:
                    raise ValueError("Individual " + str(i) + " receives no utility from their bundle. The initial bids were inconsistent with their utilities. Check that individual gets positive utility from their initial bids.")

            for j in range(self.n_goods):
                if j<self.n_linear:
                    self.bid[i, j] = self.budget[i] * (self.qty[i, j] * self.utility[i,j]) / sum_utility
                else:
                    self.bid[i, j] = (self.budget[i] * (self.qty[i, j] * self.utility[i,j]) ** self.alpha) / sum_utility
        
        self.time += 1 



# TODO: Add in functions below 
# - quasilinear
# - try to mimic what's happening there for the proportional response (with leftover money case, quasilinear). Look at zhang proof
# - constant elasticity of substitution (has already been shown to converge!)
# - Piecewise linear - stay clear of this first.