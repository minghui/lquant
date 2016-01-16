# coding=utf-8
__author__ = 'squall'

import numpy as np
import pandas as pd
import talib
# from backtest.utils.mysql import MySQLUtils

"""
This file contain all the method used for parsing OHLC data.
"""


class OHLCVD(object):
    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data
            self.dataframe = pd.DataFrame(data=data,
                                          columns=["date", "open", "high", "low", "close", "volume",
                                                   "deal"])
        elif isinstance(data, pd.DataFrame):
            self.dataframe = data
            self.data = data.values
        elif isinstance(data, list):
            self.data = np.array(data)
            self.dataframe = pd.DataFrame(data=data,
                                          columns=["date", "open", "high", "low", "close", "volume",
                                                   "deal"])
        else:
            raise ValueError("Do not support type")
        if self.data.shape[1] != 7:
            raise ValueError("Wrong shape of the data")
        self._inputs = {
            'open': data[:, 1].astype(np.float64),
            'high': data[:, 2].astype(np.float64),
            'low': data[:, 3].astype(np.float64),
            'close': data[:, 4].astype(np.float64),
            'volume': np.exp(data[:, 5].astype(np.float64))
        }

    def current_time(self):
        return self.data[-1, 0]

    def current_price(self):
        return self.data[-1, 4]

    def get_dataframe(self):
        self.dataframe

    def get_array(self):
        return self.data

    def set_config(self, config_name):

        def read_config(config_file):
            pass

        pass

    def add_macd(self):
        macd_result = talib.abstract.MACD(self._inputs)
        macd_result = np.vstack(macd_result).T
        macd_result = np.hstack((self.data, macd_result))
        self.dataframe = pd.DataFrame(data=macd_result,
                                      columns=["date", "open", "high", "low", "close", "volume",
                                               "deal", "dea", "dma", "dif"],
                                      index=self.dataframe.date)
        self.data = self.dataframe.values
        return True


