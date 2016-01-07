# coding=utf-8

import numpy as np

from backtest.BackTest import BackTestBase
from backtest.algorithm.StrategyBase import StrategyBase
from backtest.algorithm.data.record import Record


class mystrategy(StrategyBase):

    def __init__(self):
        StrategyBase.__init__(self)

    def if_buy(self, data):
        if data[4] > 10:
            return True

    def buy(self, stock_name, data):
        number = np.floor(self._fund /(data[4]*100))
        price = data[4]
        self._fund = self._fund - number*price*100
        record = Record(price=price, number=number, name=stock_name, date=data[1], tax=0, buy=True, sell=False)
        self._buy_container.add_record(record)
        return record

    def if_sell(self, data):
        if data[4] > 15:
            return True
        return False

    def sell(self, stock_name, data):
        record = self._buy_container.get_record(stock_name)
        sell_record = Record(name=stock_name, price=data[4], number=record.number, tax=0, sell=True)
        record -= sell_record

if __name__ == '__main__':
    test_case = BackTestBase(config_file='./test_backtest.yaml')
    test_strategy = mystrategy()
    test_strategy.set_data_need(1)
    test_case.set_strategy(test_strategy)
    test_case.test_strategy()