# coding=utf-8
__author__ = 'squall'


import numpy as np
import scipy as sp
import pandas as pd
from scipy.spatial.distance import *
from backtest.utils.mysql import MySQLUtils

db = MySQLUtils('root', '1988', 'test', 'stock')
data1 = db.select_data('sh600741', begin='2010-01-01', end='2015-12-30')
data_frame = db.get_dataframe('sh600741', begin='2010-01-01', end='2015-12-30')
data_frame = data_frame.set_index(data_frame.date)

data_frame1 = db.get_dataframe('sh601668', begin='2010-01-01', end='2015-12-30')
data_frame1 = data_frame1.set_index(data_frame1.date.values)


def raise_value(data_frame):
    values = data_frame.close.values
    first_day = values[:-1]
    second_day = values[1:]
    raise_rate = (second_day-first_day)/first_day*100
    result = pd.DataFrame(data=raise_rate, index=data_frame.date.values[1:])
    return result

base_data1 = raise_value(data_frame)
base_data2 = raise_value(data_frame1)

result = pd.merge(base_data1, base_data2, left_index=True, right_index=True, how='inner')


def window_similarity(data_frame, frame_len=20, frame_move=10):
    result = []
    value = data_frame.values
    for i in range(0, value.shape[0]-frame_len, frame_move):
        tmp_value = value[i:i+frame_len, :]
        cor_value = correlation(tmp_value[:, 0], tmp_value[:, 1])
        print cor_value
        result.append(cor_value)
    return result

result = window_similarity(result)

fft_result = np.abs(np.fft.fft(result))
from matplotlib import pylab as plt
plt.plot(fft_result)
plt.show()

