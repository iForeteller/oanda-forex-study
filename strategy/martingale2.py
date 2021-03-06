from strategy.strategy import Strategy


class MARTIN2(Strategy):
    def __init__(self, status):
        super(MARTIN2, self).__init__(status)
        self.martin_diff = 0.0003
        self.spread = 0.00005
        
        self.martin_init_price = 1000

        self.martin_price = self.martin_init_price
        self.status["units"] =  self.martin_init_price

    def calc_martin(self, timeseries, event):
        self.status["units"] =  self.martin_init_price
        
    def calc_pnl(self, event):
        if self.status["position"] > 0:
            return event.bid - self.status["opening_price"] - self.spread
        else:
            return self.status["opening_price"] - event.bid - self.spread

    def martin_close_condition(self, event):
        if self.calc_pnl(event) > self.martin_diff:
            self.status["units"] = abs(self.status["position"])
            self.martin_price = self.martin_init_price
            return True
        elif self.calc_pnl(event) < -self.martin_diff:
            if self.martin_price == self.martin_init_price:
                self.martin_price *= 2
                self.status["units"] = self.martin_price
            print("Martingale reverse!! %s" % (self.martin_price))
            return True
        else:
            return False
