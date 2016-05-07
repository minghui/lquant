# coding=utf-8
__author__ = 'squall'


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

data = pd.read_csv('d:/stock/new-data/sh600069.txt', sep='\t')
min_data = data.get(["OPEN", "CLOSE"]).values.max(axis=1)
real_pillar = data.OPEN.values - data.CLOSE.values
down_side = min_data - data.LOW.values
result = []
for x, y, z in zip(down_side[1:], real_pillar[1:], data.CLOSE.values[:-1]):
    if y != 0.0:
        result.append(x/z)
# print result


down_up_rate = down_side/real_pillar
result = []
for c, d, i in zip(data.CLOSE.values[:-1], down_side, data.DATE.values[1:]):
    result.append([d/c*100,c])
result = np.array(result)
rate_result = []
for i in range(len(result)-5):
    if result[i, 0] > 5:
        rate_result.append((np.max(result[i+1:i+5, 1]) - result[i, 1])/result[i, 1]*100)

rate_result = np.array(rate_result)
a = np.sum(rate_result>2)
b = rate_result.shape[0]
print a, b
print a*1.0/b
print 'this is the mean', np.mean(rate_result)
plt.plot(rate_result)