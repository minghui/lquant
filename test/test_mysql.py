# coding=utf-8
__author__ = 'squall'

import numpy as np

from backtest.utils.mysql import MySQLUtils
from data.ohlc import OHLCVD

if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'stock', 'stock')
    result = db.get_array('sh600741', begin='2007-10-10', end='2015-12-12')
    ohlc = OHLCVD(data=result)
    ohlc.add_macd()
    ohlc.add_fall_days(5)
    ohlc.add_raise_day(5)
    ohlc.add_raise_day(3)
    ohlc.add_ma(60)
    ohlc.add_jump_empty_down()
    ohlc.normalize()

    print ohlc.columns
    print ohlc.data_frame.jump_empty_down
    x = ohlc.norm_data
    y = ohlc.feature_return(5)
    x = x[:y.shape[0], :]
    print 'this is x data: ', x
    y = (y>0.10).astype(np.float64)
    from sklearn.svm import SVC
    print x.shape
    svc = SVC()
    print svc
    train_x = x[:-100, :]
    train_y = y[:-100]
    test_x = x[-100:, :]
    test_y = y[-100:]
    svc.fit(x, y)
    result = svc.predict(test_x)
    print np.sum(result == test_y)*1.0/y.shape[0]
    # vol_values = ohlc.data_frame.volume.values
    # raise_data = ohlc.data_frame.raise_rate.values
    # cor = np.correlate(vol_values, raise_data)
    # index = np.where(vol_values == np.nan)
    # print ohlc.data_frame.raise_days_3.values

    # ohlc.data_frame.plot()
    # from matplotlib import pylab as plt
    # plt.show()