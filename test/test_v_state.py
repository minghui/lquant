# coding=utf-8
__author__ = 'squall'


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

total = 0
total_event = 0
final_result = []
for roots, _, files in os.walk('d:/stock/new-data'):
    for f in files:

        file_path = os.path.join(roots, f)
        try:
            data = pd.read_csv(file_path, sep='\t')
            if data.values.shape[0] > 100:
                total_event += data.values.shape[0]
                min_data = data.get(["OPEN", "CLOSE"]).values.min(axis=1)
                real_pillar = data.OPEN.values - data.CLOSE.values
                down_side = min_data - data.LOW.values
                result = []
                for x, y, z in zip(down_side[1:], real_pillar[1:], data.CLOSE.values[:-1]):
                    if y != 0.0:
                        result.append(x/z)
                # print result


                down_up_rate = down_side/real_pillar
                result = []

                days = []
                for c, d, t, h, i in zip(data.CLOSE.values[:-1], down_side[1:], data.CLOSE.values[1:],
                                      data.HIGH.values[1:],
                                      data.DATE.values[1:]):
                    result.append([d/c*100, t, h])
                    days.append(i)

                result = np.array(result)
                rate_result = []
                for i in range(len(result)-5):
                    if result[i, 0] > 5:
                        rate_result.append((np.max(result[i+1:i+5, 2]) - result[i, 1])/result[i, 1]*100)
                        # print days[i]

                rate_result = np.array(rate_result)
                a = np.sum(rate_result>2)
                # print np.where(rate_result>2)
                b = rate_result.shape[0]
                # print a, b
                # print a*1.0/b
                total += b
                # print 'this is the mean', np.mean(rate_result)
                final_result.append(np.mean(rate_result))
                print f
        except Exception as e:
            print e.message
# plt.plot(rate_result)
print total
print total_event
plt.hist(final_result, bins=100)
plt.show()