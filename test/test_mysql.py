# coding=utf-8
__author__ = 'squall'

from backtest.utils.mysql import MySQLUtils
from backtest.data.ohlc import OHLCVD
import numpy as np


if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'test', 'stock')
    result = db.get_array('sh600741', begin='2007-10-10', end='2015-12-12')
    ohlc = OHLCVD(data=result)
    ohlc.add_macd()
    ohlc.add_fall_days(5)
    ohlc.add_raise_day(5)
    ohlc.add_raise_day(3)
    print ohlc.columns
    vol_values = ohlc.data_frame.volume.values
    raise_data = ohlc.data_frame.raise_rate.values
    cor = np.correlate(vol_values, raise_data)
    index = np.where(vol_values == np.nan)
    # print ohlc.data_frame.raise_days_3.values

    # ohlc.data_frame.plot()
    # from matplotlib import pylab as plt
    # plt.show()