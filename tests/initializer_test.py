import unittest
from root.initializer import Initializer
from root.market import Market

class InitializerBasicTest:
    def test(self):
        initializer = Initializer(100, 100)
        params = initializer.initialize_linear_utilities_basic()
        print(params)
        market = Market(params[0], params[1], params[2])
        for i in range(10):
            print(market.get_qty())
            market.prop_resp_update()