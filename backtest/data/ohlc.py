# coding=utf-8
__author__ = 'squall'

import numpy as np
import pandas as pd
import talib
import codecs
import yaml
# from backtest.utils.mysql import MySQLUtils

"""
This file contain all the method used for parsing OHLC data.
"""


class OHLCVD(object):
    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data
            self.data_frame = pd.DataFrame(data=data,
                                           columns=["date", "open", "high", "low", "close",
                                                    "volume",
                                                    "deal"])
        elif isinstance(data, pd.DataFrame):
            self.data_frame = data
            self.data = data.values
        elif isinstance(data, list):
            self.data = np.array(data)
            self.data_frame = pd.DataFrame(data=data,
                                           columns=["date", "open", "high", "low", "close",
                                                    "volume",
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
        self.data_frame

    def get_array(self):
        return self.data

    def configure(self, config_name):
        """
        Add all feature we need configured by the configure file.
        :param config_name:
        :return:
        """
        # TODO: Test this method.

        def read_config(config_file):
            with codecs.open(config_file, encoding='utf-8') as f:
                config = yaml.load(f)
            return config

        config = read_config(config_name)
        for key in config:
            try:
                method = talib.get_functions(key)
                tmp_result = method(self._inputs)
                tmp_result = np.vstack(tmp_result).T
                assert tmp_result.shape[0] == self.data.shape[0]
                self.data = np.hstack((self.data, tmp_result))
            except Exception as e:
                raise ValueError(e, 'Wrong in configure')
        self.data_frame = pd.DataFrame(self.data, index=self.data_frame.date)

    def add_macd(self):
        macd_result = talib.abstract.MACD(self._inputs)
        macd_result = np.vstack(macd_result).T
        macd_result = np.hstack((self.data, macd_result))
        self.data_frame = pd.DataFrame(data=macd_result,
                                       columns=["date", "open", "high", "low", "close", "volume",
                                                "deal", "dea", "dma", "dif"],
                                       index=self.data_frame.date)
        self.data = self.data_frame.values
        return True


