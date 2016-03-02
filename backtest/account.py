# coding=utf-8

from Configurable import Configurable
from order_book import OrderBook


class Account(Configurable):
    this_key = "account"
    key_cash = "cash"

    def __init__(self, cash):
        self._cash = cash
        self._stock_dict = {}
        self._order_book = OrderBook()

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

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

    def asset(self, date):
        pass