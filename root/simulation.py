from market import Market
import warnings

class Simulation:
    """
    Class to simulate dynamics.
    Contains a market.
    Keeps track of variables at each time.
    Also has a method to run t time steps.
    
    Attributes
    ----------
    market : Market
        Market being simulated
    prices : list
        prices[t] gives price np.array at time t
    qtys : list
        qtys[t] gives qty np.array at time t
    bids: list
        bids[t] gives bid np.array at time t
    utilities: list
        utilities[t] gives individual utility np.array at time t
    
    """
    def __init__(self, market: Market):
        if (market.get_time() != 0):
            warnings.warn("Warning: Market does not have time 0 at start of simulation")

        self.market = market
        self.prices = []
        self.qtys = []
        self.bids = []
        self.utilities = []
        self.prices.append(market.get_price())
        self.qtys.append(market.get_qty())
        self.bids.append(market.get_bid())
        self.utilities.append(market.get_individual_utility())
    
    def run(self, time_steps):
        for i in range(time_steps):
            self.market.update()
            self.prices.append(self.market.get_price())
            self.qtys.append(self.market.get_qty())
            self.bids.append(self.market.get_bid())
            self.utilities.append(self.market.get_individual_utility())

    def get_prices(self):
        return self.prices

    def get_qtys(self):
        return self.qtys
    
    def get_bids(self):
        return self.bids

    def get_utilities(self):
        return self.utilities

    
        



