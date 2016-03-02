# coding=utf-8

from account import Account
from Configurable import Configurable


class OrderBook(Configurable):

    def __init__(self):
        """
        Now, do not think about the different account.
        :return:
        """
        self._account = Account()
        self._order_list = []

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def configure(self, configure, context):
        pass

    def receive_order(self, order):
        pass

    def reject(self):
        pass