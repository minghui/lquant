# coding=utf-8
__author__ = 'squall'

import talib
import numpy as np
import pandas as pd
from backtest.utils.mysql import MySQLUtils

db = MySQLUtils('root', '1988', 'test', 'stock')

data = db.get_array(id='sh600741', begin='2010-01-01', end='2016-12-31')
print data

print np.exp(data[:, 5].astype(np.float64))
# note that all ndarrays must be the same length!
inputs = {
    'open': data[:, 1].astype(np.float64),
    'high': data[:, 2].astype(np.float64),
    'low': data[:, 3].astype(np.float64),
    'close': data[:, 4].astype(np.float64),
    'volume': np.exp(data[:, 5].astype(np.float64))
}


macd_result = talib.abstract.MACD(inputs)
macd_result = np.vstack(macd_result)
macd_data_frame = pd.DataFrame(data=macd_result.T, index=data[:, 0])
x = macd_result.T
y = x[:, 1] - x[:, 0]
print y*2
# macd_data_frame.plot()
# from matplotlib import pylab as plt
# plt.show()

# print macd_data_frame
sar = talib.abstract.SAR(inputs)
sar_data_frame = pd.DataFrame(data=sar, index=data[:, 0])
print sar_data_frame
# sar_data_frame.plot()
# from matplotlib import pylab as plt
# plt.show()