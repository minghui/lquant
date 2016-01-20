# coding=utf-8
__author__ = 'squall'
from backtest.utils.mysql import MySQLUtils
from backtest.data.ohlc import OHLCVD
import numpy as np


if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'test', 'stock')
    result = db.get_array('sh600741', begin='2007-10-10', end='2015-12-12')
    ohlc = OHLCVD(data=result)
    vol_values = ohlc.data_frame.volume.values
    kernel = np.ones(20)*0.05
    result = np.convolve(kernel, vol_values, mode='valid')
    from matplotlib import pylab as plt
    plt.plot(result)
    plt.show()