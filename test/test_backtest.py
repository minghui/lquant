# coding=utf-8

import numpy as np
from matplotlib import pylab as plt

from backtest.backtest_base import BackTestBase
from algorithm.StrategyBase import StrategyBase
from data.ohlc import OHLCVD
from data.order import Order


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
        print np.sum(down < 0)
        # print 'This is the dta shape', data.shape[0]
        if np.sum(down < 0) >= data.shape[0] - 1:
            return data[-1, 4], data[-1, 0]

    def if_sell(self, data, name=None):
        record = self.stock_asset.get_order(name)
        if record is not None:
            result = (data[-1, 4] - record.price)/record.price *100
            if result > 5.0 or result < -3.0:
                return data[-1, 4], data[-1, 0]


class MaStrategy(StrategyBase):

    def __init__(self):
        StrategyBase.__init__()

    def if_buy(self, context):
        data = context.db.select_data_by_number(70, context.date)
        ohlc = OHLCVD(data)
        ohlc.add_ma(60)
        ohlc.add_ma(10)
        data_frame = ohlc.get_dataframe()
        ma60_value = data_frame.m60.values[-1]
        low = data_frame.low.values[-1]
        price = data_frame.close.values[-1]
        if (low - ma60_value) / ma60_value >= 0.2:
            number = np.floor(context.account.cash/(price*100))
            return Order(date=context.date, price=price, number=number)

    def is_sell(self):
        pass


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
