# coding=utf-8
#
import pandas as pd
import numpy as np
# from matplotlib import pylab as plt
#
# date_index = pd.date_range('2015-10-10', periods=10)
# date_index1 = pd.date_range('2015-10-08', periods=10)
# a = pd.DataFrame(data=np.random.normal(size=(10,2)), index=date_index, columns=list('cd'))
# b = pd.DataFrame(data=np.random.normal(size=(10,2)), index=date_index1, columns=list('ab'))
# pd.merge(a, b, left_index=True, right_index=True, how='inner')
#
#
# ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
# df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
#                    columns=['A', 'B', 'C', 'D'])
# df = df.cumsum()
# # plt.figure()
# df.plot()
# plt.legend(loc='best')
# plt.show()
#
#
# class test_pro(object):
#
#     def __init__(self):
#         self._score = 10
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self, data):
#         if data > 100:
#             raise ValueError("fuck")
#         self._score = data
#
#
# if __name__ == '__main__':
#     x = test_pro()
#     x.score = 25
#     print x.score
#     import tablib as tb

from datetime import datetime, timedelta

a = '20151112 12:20:00'

a = a.split(' ')
if len(a) > 1:
    date = datetime.strptime(a[0], "%Y%m%d")
print 'This is date time:', date



import numpy as np

np.mean()