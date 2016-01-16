# coding=utf-8
__author__ = 'squall'

from backtest.utils.mysql import MySQLUtils
from backtest.data.ohlc import OHLCVD

if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'test', 'stock')
    result = db.get_array('sh600741', begin='2015-10-10', end='2015-12-12')
    ohlc = OHLCVD(data=result)
    ohlc.add_macd()
    ohlc.data_frame.plot()
    from matplotlib import pylab as plt
    plt.show()