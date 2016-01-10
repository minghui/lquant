# coding=utf-8

import numpy as np

from backtest.backtest_base import BackTestBase
from backtest.algorithm.StrategyBase import StrategyBase
from backtest.trade import TradeStrategy


class mystrategy(StrategyBase):

    def __init__(self):
        StrategyBase.__init__(self)

    def if_buy(self, data):
        # print 'In if buy',
        if data[-1, 4] > 10:
            return data[-1, 4], data[-1, 0]

    def if_sell(self, data):
        if data[-1, 4] > 15:
            return data[-1, 4], data[-1, 0]
        return None

if __name__ == '__main__':
    import logging
    import os
    logging.basicConfig(level=logging.NOTSET,
                        format='%(asctime)s %(name)-12s '
                               '%(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=os.path.join('./', 'RdsInterface.log'),
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    test_case = BackTestBase(config_file='./test_backtest.yaml', log=logging)
    test_strategy = mystrategy()
    test_trade_strategy = TradeStrategy()
    test_case.init(strategy=test_strategy, trade_strategy=test_trade_strategy)
    test_case.test_strategy()
    test_case.summary()