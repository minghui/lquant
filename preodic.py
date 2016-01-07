# coding=utf-8

from backtest.BackTest import *
from backtest.algorithm.data.record import Record


class PeriodicStrategy(StrategyBase):

    def __init__(self, config_file, *argv, **kwargs):
        super(StrategyBase, self).__init__(argv, kwargs)
        with codecs.open(config_file, encoding='utf-8') as f:
            config = yaml.load(f)
        self.__dict__.update(config)
        self._buy = False
        self._begin_fund = self._fund

    def if_buy(self, stock_data):
        fall_sum = np.sum((stock_data[1:, 4] - stock_data[:-1, 4]) < 0)
        if fall_sum > self.need_data_length-1:
            return True
        else:
            return False

    def buy(self, stock_name, stock_data):
        if not self.buy:
            current_price = stock_data[-1, 4]
            buy_number = np.floor(self._fund/(current_price*100))
            cost_money = buy_number*current_price*100
            self._fund -= (cost_money + self.tax*cost_money)
            return Record(stock_name,
                          buy=True,
                          sell=False,
                          number=buy_number,
                          price=current_price,
                          tax=self.tax,
                          date=stock_data[-1, 0])

    def if_sell(self, stock_data):
        pass

    def sell(self):
        pass