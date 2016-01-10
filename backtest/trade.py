# encoding=utf-8

from backtest.algorithm.data.record_container import RecordContainer
from backtest.algorithm.data.record_container import Record
import numpy as np


class TradeStrategy(object):
    """
    This is t he buy strategy base class.
    """

    def __init__(self):
        self._fund = None
        # for every stock we have a container
        self.stock_asset = RecordContainer()
        self.asset_daliy = None
        self._sell_record_list = []
        self._buy_record_list = []

    def init(self, fund):
        self._fund = fund
        self.stock_asset.clear()
        self.asset_daliy = []

    def buy_strategy(self, *argv, **kwargs):
        """
        Here is just a sample buy strategy.
        :param data:
        :return:
        """
        name = kwargs.get('name')
        price = kwargs.get("price")
        date = kwargs.get("date")
        number = np.floor(self._fund / (price * 100))
        if number != 0:
            self._fund -= price * number * 100
            record = Record(name=name, date=date,
                            number=number, price=price, tax=0, buy=True)
            self.stock_asset.add_record(record)
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
        record = self.stock_asset.get_record(name)
        if record is not None:
            sell_record = Record(name=name, date=date,
                                 price=price, number=record.number,
                                 tax=0, sell=True)
            print 'This is the sell record:', sell_record
            self._fund += record.number * price * 100
            self.stock_asset.add_record(sell_record)
            self._sell_record_list.append(sell_record)
            return True
        return False

    def get_assert(self, stock, data):
        record = self.stock_asset.get_record(stock)
        if record is not None:
            current_asset = self._fund + record.number * data[4] * 100
        else:
            current_asset = self._fund
        print record
        print 'current stock:', current_asset, 'current fund: ', self._fund
        self.asset_daliy.append(current_asset)

    def get_asset_daliy(self):
        return self.asset_daliy