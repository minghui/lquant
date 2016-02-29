# coding=utf-8

from account import Account
from Configurable import Configurable


class OrderBook(Configurable):

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def configure(self, configure, context):
        pass

    def __init__(self):
        self._account = Account()