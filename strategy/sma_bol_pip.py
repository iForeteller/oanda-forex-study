from strategy.sma import SMA
from strategy.pip import PIP
from strategy.bol import BOL
from strategy.time import Time


class SMABOLPIP(SMA, PIP, Time, BOL):
    def __init__(self, status):
        SMA.__init__(self, status)
        PIP.__init__(self, status)
        BOL.__init__(self, status)        

    def calc_indicator(self, timeseries, event):
        self.calc_sma(timeseries, event)
        self.calc_pip_over_closs(timeseries, event)
        self.calc_pip_mean(timeseries, event)
        self.calc_bol(timeseries, event)

    def buy_condition(self):
        return self.sma_buy_condition() \
            or self.bol_buy_condition()

    def close_buy_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            or self.pip_loss_cut_condition(event) \
            and not self.time_guard_condition(event)

    def sell_condition(self):
        return self.sma_sell_condition() \
            or self.bol_sell_condition()
    
    def close_sell_condition(self, event):
        return self.pip_expand_close_condition(event) \
            or self.pip_over_cross_condiiton(event) \
            or self.pip_loss_cut_condition(event) \
            and not self.time_guard_condition(event)
