# coding=utf-8

import numpy as np
from matplotlib import pylab as plt

from backtest.backtest_base import BackTestBase
from algorithm import StrategyBase


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


def analysis(context):
    for x in context:
        context[x]["return"].plot()
        plt.show()


class CountStrategy(StrategyBase):

    def __init__(self):
        StrategyBase.__init__(self)

    def if_buy(self, data, name=None):
        down = data[1:, 4] - data[:-1, 4]
        print np.sum(down<0)
        # print 'This is the dta shape', data.shape[0]
        if np.sum(down<0) >= data.shape[0]-1:
            return data[-1, 4], data[-1, 0]

    def if_sell(self, data, name=None):
        record = self.stock_asset.get_record(name)
        if record is not None:
            result = (data[-1, 4] - record.price)/record.price *100
            if result > 5.0 or result < -3.0:
                return data[-1, 4], data[-1, 0]


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
    test_strategy = CountStrategy()
    test_case.init(strategy=test_strategy, analysis=analysis)
    test_case.test_strategy()
