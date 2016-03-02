# coding=utf-8

from abc import abstractmethod

from data.record_container import OrderBook
from backtest.utils.tax import *
from data.order import Order


class StrategyBase(object):

    def __init__(self):
        """
        Load buy strategy and sell strategy.
        """
        # record the buy and sell
        self._data_need = None
        self._fund = 0
        # for every stock we have a container
        self.stock_asset = OrderBook()
        self.asset_daliy = None
        self._sell_record_list = []
        self._buy_record_list = []

    def init(self, fund):
        self._fund = fund
        self.stock_asset.clear()
        self.asset_daliy = []

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
        Check if buy stock.
        :param argv:
        :param kwargs:
        :return: first is price, second is date
        """
        return None, None


    @abstractmethod
    def if_sell(self, *argv, **kwargs):
        """
        Check if sell the stock.
        :param argv:
        :param kwargs:
        :return: fist is price, second is date
        """
        return None, None

    @abstractmethod
    def summary(self, *argv, **kwargs):
        """
        Summary the buy and sell, get return.
        :param argv:
        :param kwargs:
        :return:
        """
        pass

    def buy_strategy(self, *argv, **kwargs):
        """
        Here is just a sample buy strategy.
        :param data:
        :return:
        """
        # print 'go here'
        name = kwargs.get('name')
        price = kwargs.get("price")
        date = kwargs.get("date")
        tax = kwargs.get("tax")
        number = max_buy_number(self._fund, price, tax)
        if number != 0:
            self._fund -= price*(1+tax)*number*100
            cost_tax = price*number*100*0.001
            record = Order(name=name, date=date,
                            number=number, price=price, tax=cost_tax, buy=True)
            print 'This is the buy record: ', record
            self.stock_asset.add_order(record)
            self._buy_record_list.append(record)
            return True
        return False

    def sell_strategy(self, *args, **kwargs):

        """
        Here is just a sample sell strategy.
        # TODO: Sell strategy should be configable.
        :param data:
        :return: True or False
        """
        name = kwargs.get('name')
        price = kwargs.get("price")
        date = kwargs.get('date')
        tax = kwargs.get("tax")
        record = self.stock_asset.get_order(name)
        if record is not None and record.number > 0:

            sell_record = Order(name=name, date=date,
                                 price=price, number=record.number,
                                 tax=0, sell=True)
            print 'This is the sell record:', sell_record
            self._fund += record.number * price * 100*(1-tax)
            self.stock_asset.add_order(sell_record)
            self._sell_record_list.append(sell_record)
            return True
        return False

    def get_asset(self, stock, data):
        record = self.stock_asset.get_order(stock)
        if record is not None:
            current_asset = self._fund + record.number * data[4] * 100
        else:
            current_asset = self._fund
        # print 'This is get assert', record
        # print 'current stock:', record , 'current fund: ', self._fund
        self.asset_daliy.append(current_asset)

    def get_asset_daliy(self):
        return self.asset_daliy

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
