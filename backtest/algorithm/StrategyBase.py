# coding=utf-8

from abc import abstractmethod
from data.record_container import RecordContainer


class StrategyBase(object):

    def __init__(self):
        """
        Load buy strategy and sell strategy.
        """
        # record the buy and sell
        self._all_record = []
        self._buy_record = []
        self._sell_record = []
        self._buy_container = RecordContainer()
        self._sell_container = RecordContainer()
        self._data_need = None
        self._fund = 0

    def init(self, fund):
        self._fund = fund

    def get_data_need(self):
        """
        One strategy must know how much data it need, it help backtest.
        """
        return self._data_need

    def set_data_need(self, length):
        self._data_need = length

    @abstractmethod
    def if_buy(self, *argv, **kwargs):
        """
        A strategy much contain buy strategy.
        """
        pass


    @abstractmethod
    def if_sell(self, *argv, **kwargs):
        """
        Check if sell the stock.
        :param argv:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def summary(self, *argv, **kwargs):
        """
        Summary the buy and sell, get return.
        :param argv:
        :param kwargs:
        :return:
        """
        pass


# class BuyStrategyBase(object):
#     """
#     Basic Buy strategy.
#     """
#
#     def __init__(self, *argc, **kwargs):
#         self._total_money = None
#         pass
#
#     def if_buy(self, data):
#         pass
#
#     def check_money(self):
#         pass
#
#     def buy(self):
#         pass
#
#     def add_record(self):
#         pass
#
#     def load_strategy(self, file_name):
#         pass
#
#
# class SellStrategyBase(object):
#     """
#     Basic sell strategy.
#     """
#
#     def __init__(self, *argc, **kwargs):
#         pass
#
#     def if_sell(self, data):
#         pass
#
#     def check_money(self):
#         pass
#
#     def sell(self):
#         pass
#
#     def add_record(self):
#         pass
