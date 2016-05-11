# coding=utf-8
__author__ = 'squall'

import numpy as np

from backtest.utils.mysql import MySQLUtils
from data.ohlc import OHLCVD


def prepare_data(db, stock_list, begin, end):
    results = []
    labels = []
    for stock in stock_list:
        tmp_result = db.get_array(stock, begin=begin, end=end)
        print stock
        if tmp_result.shape[0] > 100:
            ohlc = OHLCVD(data=tmp_result)
            ohlc.add_macd()
            ohlc.add_fall_days(5)
            ohlc.add_raise_day(5)
            ohlc.add_raise_day(3)
            ohlc.add_ma(60)
            # ohlc.add_rsi_feature()
            ohlc.add_jump_empty_down()
            ohlc.normalize()
            results.append(ohlc.data)
            label = ohlc.future_return(5)
            labels.append(label)
        print len(results)
        print len(labels)
    return results


if __name__ == '__main__':
    db = MySQLUtils('root', '1988', 'stock', 'stock_with_feature')
    import pandas as pd
    data = pd.read_csv('d:/stock/new-data/sh600741.txt', sep='\t')
    result = OHLCVD(data.values)
    result.add_all_ta_feature()
    result = result.data_frame.replace(np.nan, -1.0).replace(np.inf, -2.0).replace(-np.inf, -3.0)
    db_name = "stock_with_feature"
    db.create_feature_db(db_name)
    db.insert_feature_data(db_name, result.values, 'sh600741')
    # result = db.get_array('sh600741', begin='2007-10-10', end='2015-12-12')
    # ohlc = OHLCVD(data=result)
    # ohlc.add_macd()
    # ohlc.add_fall_days(5)
    # ohlc.add_raise_day(5)
    # ohlc.add_raise_day(3)
    # ohlc.add_ma(60)
    # ohlc.add_jump_empty_down()
    # ohlc.normalize()
    #
    # print ohlc.columns
    # print ohlc.data_frame.jump_empty_down
    # x = ohlc.norm_data
    # y = ohlc.feature_return(5)
    # x = x[:y.shape[0], :]
    # print 'this is x data: ', x
    # y = (y>0.10).astype(np.float64)
    # from sklearn.svm import SVC
    # print x.shape
    # svc = SVC()
    # print svc
    # train_x = x[:-100, :]
    # train_y = y[:-100]
    # test_x = x[-100:, :]
    # test_y = y[-100:]
    # svc.fit(x, y)
    # result = svc.predict(test_x)
    # print np.sum(result == test_y)*1.0/y.shape[0]
    # vol_values = ohlc.data_frame.volume.values
    # raise_data = ohlc.data_frame.raise_rate.values
    # cor = np.correlate(vol_values, raise_data)
    # index = np.where(vol_values == np.nan)
    # print ohlc.data_frame.raise_days_3.values

    # ohlc.data_frame.plot()
    # from matplotlib import pylab as plt
    # plt.show()