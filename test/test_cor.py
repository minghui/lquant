# coding=utf-8
__author__ = 'squall'


import numpy as np
import scipy as sp
import pandas as pd
from scipy.spatial.distance import *
from backtest.utils.mysql import MySQLUtils


def raise_value(data_frame):
    values = data_frame.close.values
    first_day = values[:-1]
    second_day = values[1:]
    raise_rate = (second_day-first_day)/first_day*100
    result = pd.DataFrame(data=raise_rate, index=data_frame.date.values[1:])
    return result


def window_similarity(data_frame, frame_len=20, frame_move=10):
    result = []
    value = data_frame.values
    for i in range(0, value.shape[0]-frame_len, frame_move):
        tmp_value = value[i:i+frame_len, :]
        cor_value = correlation(tmp_value[:, 0], tmp_value[:, 1])
        result.append(cor_value)
    return result

db = MySQLUtils('root', '1988', 'test', 'stock')
stock_lists = db.execute_sql("SELECT DISTINCT ID FROM STOCK")
stock_lists = [x[0] for x in stock_lists]


def iter_over_stocks(stock_lists, db):
    final_result = {}
    for x in stock_lists:
        for y in stock_lists:
            data1 = db.select_data(stock_lists[0], begin='2010-01-01', end='2015-12-30')
            data_frame = db.get_dataframe('sh600741', begin='2010-01-01', end='2015-12-30')
            data_frame = data_frame.set_index(data_frame.date)

            data_frame1 = db.get_dataframe('sh601668', begin='2010-01-01', end='2015-12-30')
            data_frame1 = data_frame1.set_index(data_frame1.date.values)



            base_data1 = raise_value(data_frame)
            base_data2 = raise_value(data_frame1)

            result = pd.merge(base_data1, base_data2, left_index=True, right_index=True, how='inner')
            result = window_similarity(result)
            final_result.update({x + y: result})
    return final_result

result = iter_over_stocks(stock_lists[0:500], db)
import cPickle
cPickle.dump(result, open('d:/baidu/simi.p', 'wb'))

