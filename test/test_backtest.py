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

    def if_sell(self, data):
        if data[4] > 15:
            return True
        return False

if __name__ == '__main__':
    test_case = BackTestBase(config_file='./test_backtest.yaml')
    test_strategy = mystrategy()
    test_strategy.set_data_need(1)
    test_case.set_strategy(test_strategy)
    test_case.test_strategy()
    test_case.summary()