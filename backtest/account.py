# coding=utf-8

from Configurable import Configurable
from order_book import OrderBook


class Account(object):
    this_key = "account"
    key_cash = "cash"

    def __init__(self, cash):
        self._origin_cash = cash
        self._cash = cash
        self._stock_asset = {}
        self._order_book = OrderBook()
        self._daliy_asset = {}
        self._current_positon = None
        self._daliy_positon = {}
        self._dbbase = None

    def init_from_config(self, config, **kwargs):
        if self.this_key in config:
            config_dict = config[self.this_key]
        else:
            raise ValueError("Do not have the key")
        self._cash = config_dict[self.key_cash]

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        self._cash = cash

    def add_cash(self, added_cash):
        self._cash = added_cash

    def reset(self):
        pass

    def get_asset(self, date):
        stock_asset = 0
        for key in self._stock_asset:
            current_price = self._dbbase.get(key, date)
            self._stock_asset[key].current_price = current_price
            stock_asset += self._stock_asset[key].current_price * \
                           self._stock_asset[key].number
        return self._cash + stock_asset

    def position(self):
        return self._cash / self._origin_cash

    def buy(self, order, market=None):
        if market is None:
            raise ValueError("Invalid market")
        if order.cost > self._cash:
            raise ValueError("Do not have so much money")
        if market.process_order(order):
            self._order_book.add_order(order)
            if order.name in self._stock_asset:
                self._stock_asset[order.name] += order
        else:
            return False

    def sell(self, order, market=None):
        if market is None:
            raise ValueError("Invalid market")
        if order.name not in self._stock_asset:
            raise ValueError("Can sell do not have stock asset")
        if order.number > self._stock_asset[order.name].number:
            raise ValueError("Can not sell too much")
        if market.process_order(order):
            self._order_book.add_order(order)
            self._stock_asset[order.name] += order
            return True
        else:
            return False

    def _after_market(self, date):
        for key in self._stock_asset:
            current_price = self._dbbase.get(key, date)
            self._stock_asset[key].current_price = current_price

    def _update_asset(self, date):

        for key in self._stock_asset:
            stock_asset = self._stock_asset[key]
            data = self._dbbase.get(stock_asset.name, date)
            stock_asset.current_price = data
