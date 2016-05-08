# coding=utf-8
__author__ = 'squall'

import numpy as np
import pandas as pd
import talib
import codecs
import yaml
import logging
from sklearn.preprocessing import normalize


logger = logging.getLogger("ohlc")

"""
This file contain all the method used for parsing OHLC data.
"""


class OHLCVD(object):

    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data
            self.data_frame = pd.DataFrame(data=data,
                                           columns=["date", "open", "high",
                                                    "low", "close",
                                                    "volume",
                                                    "deal"])
        elif isinstance(data, pd.DataFrame):
            self.data_frame = data
            self.data = data.values
        elif isinstance(data, list):
            self.data = np.array(data)
            self.data_frame = pd.DataFrame(data=data,
                                           columns=["date", "open", "high",
                                                    "low", "close",
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
        self.columns = ["date", "open", "high", "low", "close", "volume",
                        "deal"]

    def current_time(self):
        return self.data[-1, 0]

    def current_price(self):
        return self.data[-1, 4]

    def get_dataframe(self):
        return self.data_frame

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
        """
        Some method can be refactor.
        :return:
        """
        macd_result = talib.abstract.MACD(self._inputs)
        macd_result = np.vstack(macd_result).T
        macd_result = np.hstack((self.data, macd_result))
        self.columns = self.columns + ["dea", "dma", "dif"]
        self.data_frame = pd.DataFrame(data=macd_result,
                                       columns=self.columns,
                                       index=self.data_frame.date)
        self.data = self.data_frame.values
        return True

    def add_ma(self, length):
        ma = talib.abstract.MA(self._inputs, timeperiods=length)
        ma = ma.reshape((ma.shape[0], 1))
        ma = np.hstack((self.data, ma))
        self.columns = self.columns + ["ma"+str(length)]
        self.data_frame = pd.DataFrame(data=ma,
                                       columns=self.columns,
                                       index=self.data_frame.date)
        self.data = self.data_frame.values
        return True

    def add_sar(self):
        sar_result = talib.abstract.SAR(self._inputs)
        sar_result = np.vstack(sar_result).T
        sar_result = np.hstack((self.data, sar_result))
        self.columns = self.columns + ['sar']
        self.data_frame = pd.DataFrame(data=sar_result,
                                       columns=self.columns,
                                       index=self.data_frame.date)
        self.data = self.data_frame.values
        return True

    def add_specified_feature(self, feature_name, column_name, parameters=None):
        """
        Use this method to extract all the feature we can get from talib.
        :param feature_name:
        :param column_name:
        :param parameters:
        :return:
        """
        # TODO: Test if this method work.
        extract_method = talib.get_functions(feature_name)
        if parameters is not None and isinstance(parameters, dict):
            feature = extract_method(self._inputs, parameters)
        else:
            feature = extract_method(self._inputs)
        feature = np.vstack(feature).T
        self.data = np.hstack((self.data, feature))
        self.columns = self.columns + column_name
        self.data_frame = pd.DataFrame(data=self.data,
                                       columns=self.columns,
                                       index=self.data_frame.date)
        return True

    def add_raise(self):
        close_data = self.data_frame.close.values
        result = (close_data[1:] - close_data[0:-1])/close_data[0:-1]*100
        result = np.array([np.nan] + result.tolist())
        result = result.reshape(result.shape[0], 1)
        self.data = np.hstack((self.data, result))
        self.columns.append("raise_rate")
        self.data_frame = pd.DataFrame(data=self.data,
                                       columns=self.columns,
                                       index=self.data_frame.date)
        return True

    def add_raise_day(self, n):
        if "raise_rate" not in self.columns:
            self.add_raise()
        data = self.data_frame.raise_rate.values
        data = (data > 0).astype(np.float64)
        kernel = np.ones(n)
        result = np.convolve(kernel, data, 'valid')
        result = np.array([np.nan]*(n-1) + result.tolist())
        result = result.reshape(result.shape[0], 1)
        self._add_new_feature(result, "raise_days_"+str(n))
        return True

    def add_fall_days(self, n):
        if "raise_rate" not in self.columns:
            self.add_raise()
        data = self.data_frame.raise_rate.values
        data = (data < 0).astype(np.float64)
        kernel = np.ones(n)
        result = np.convolve(kernel, data, 'valid')
        result = np.array([np.nan]*(n-1) + result.tolist())
        result = result.reshape(result.shape[0], 1)
        self._add_new_feature(result, "fall_days_"+str(n))

    def add_jump_empty_down(self):
        close_data = self.data_frame.close.values
        open_data = self.data_frame.open.values
        indicator = open_data[1:] - close_data[:-1]
        indicator = (indicator < 0).astype(np.float64)
        indicator = np.array([0] + indicator.tolist())
        indicator = indicator.reshape((indicator.shape[0], 1))
        self._add_new_feature(indicator, "jump_empty_down")

    def add_jump_empty_up(self):
        close_data = self.data_frame.close.values
        open_data = self.data_frame.open.values
        indicator = open_data[1:] - close_data[:-1]
        indicator = (indicator > 0).astype(np.float64)
        indicator = np.array([0] + indicator.tolist())
        indicator = indicator.reshape((indicator.shape[0], 1))
        self._add_new_feature(indicator, "jump_empty_up")

    def add_rsi_feature(self):
        inputs = {
            'open': self.data_frame.open.values.astype(np.float64),
            'high': self.data_frame.high.values.astype(np.float64),
            'low': self.data_frame.low.values.astype(np.float64),
            'close': self.data_frame.close.values.astype(np.float64),
            'volume': self.data_frame.volume.values.astype(np.float64)
        }
        print 'self.data.shape is :', self.data.shape
        tmp = talib.abstract.RSI(inputs, timeperiod=6)

        tmp = tmp.reshape((tmp.shape[0], 1))
        self._add_new_feature(tmp, "rsi6")
        tmp = talib.abstract.RSI(inputs, timeperiod=12)
        tmp = tmp.reshape(tmp.shape[0], 1)
        self._add_new_feature(tmp, "rsi12")
        tmp = talib.abstract.RSI(inputs, timeperiod=24)
        tmp = tmp.reshape(tmp.shape[0], 1)
        self._add_new_feature(tmp, "rsi24")

    def add_recent_down_v_turn(self, n):
        """
        If recent n days appear down v turn event.
        :param n:
        :return:
        """
        min_price = np.min(self.data_frame.get(["open", "close"]).values, axis=1)
        low_price = self.data_frame_frame.low.values
        xuti = min_price - low_price
        v_state = xuti[1:]/low_price[:-1]
        np.concatenate(([0], v_state), axis=0)
        self._add_new_feature(v_state, "v_state")

    def normalize(self):
        norm_data = self.data[:, 1:]
        norm_data = norm_data.astype(np.float64)
        norm_data[np.isnan(norm_data)] = 0
        norm_data = (norm_data - norm_data.mean(0))/norm_data.std(0)
        self.norm_data = norm_data

    def future_return(self, n_days=5):
        close_value = self.data_frame.close.values
        return_rate = (close_value[n_days:] - close_value[:-n_days])/\
                      close_value[:-n_days]
        return return_rate

    def __getitem__(self, item):
        pass

    def _add_new_feature(self, data, columns):
        print self.data.shape
        self.data = np.hstack((self.data, data))
        if isinstance(columns, list):
            self.columns = self.columns + columns
        elif isinstance(columns, str):
            self.columns.append(columns)
        else:
            raise ValueError("Wrong type of columns")
        self.data_frame = pd.DataFrame(data=self.data,
                                       columns=self.columns,
                                       index=self.data_frame.date)


if __name__ == '__main__':
    pass