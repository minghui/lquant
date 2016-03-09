# coding=utf-8
__author__ = 'squall'
import numpy as np

from backtest.utils.mysql import MySQLUtils
from data.ohlc import OHLCVD

if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'stock', 'stock')
    result = db.get_array('sh600741', begin='2007-10-10', end='2015-12-12')
    ohlc = OHLCVD(data=result)
    print result
    print ohlc.get_dataframe()
    ohlc.add_macd()
    ohlc.add_ma(60)
    print ohlc.get_array().shape
    print ohlc.get_dataframe()
    vol_values = ohlc.data_frame.volume.values
    kernel = np.ones(20)*0.05
    result = np.convolve(kernel, vol_values, mode='valid')
    # plt.plot(result)
    # plt.show()