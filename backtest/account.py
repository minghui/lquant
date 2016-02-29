# coding=utf-8

from Configurable import Configurable
from order_book import OrderBook


class Account(Configurable):

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def __init__(self, cash):
        self._cash = cash
        self._stock_dict = {}
        self._order_book = OrderBook()

    @property
    def get_cash(self):
        return self._cash

    @property
    def set_cash(self, cash):
        self._cash = cash

    def add_cash(self, added_cash):
        self._cash = added_cash

    def configure(self, configure, context):
        pass

    @staticmethod
    def get_from_context(context, key):
        context.get_object(key)