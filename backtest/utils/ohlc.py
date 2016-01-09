# coding=utf-8
__author__ = 'squall'

import numpy as np
import pandas as pd
"""
This file contain all the method used for parsing OHLC data.
"""


class OHLCVD(object):

    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data
            self.dataframe = pd.DataFrame(data=data, columns=["date", "open", "high", "low", "close", "volume", "deal"])
        elif isinstance(data, pd.DataFrame):
            self.dataframe = data
            self.data = data.values
        elif isinstance(data, list):
            self.data = np.array(data)
            self.dataframe = pd.DataFrame(data=data, columns=["date", "open", "high", "low", "close", "volume", "deal"])
        else:
            raise ValueError("Do not support type")
        if self.data.shape[1] != 7:
            raise ValueError("Wrong shape of the data")

    def current_time(self):
        return self.data[-1, 0]

    def current_price(self):
        return self.data[-1, 4]

    def get_dataframe(self):
        self.dataframe

    def get_array(self):
        return self.data

