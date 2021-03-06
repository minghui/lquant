# coding=utf-8

"""
This is the market object, this object is used to simulate the real stock market.
We can initialize this object by a yaml config file, which contain the type of
the market, such as T+1 or T+0
"""

from Configurable import Configurable
from order_book import OrderBook
from account import Account
from backtest.utils.utils import get_module_logger

logger = get_module_logger(__name__)


class Market(Configurable):

    def __init__(self):
        self._account = None
        self._order_book = None

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def configure(self, configure, context):
        self._account = Account()
        self._order_book = OrderBook()

    def process_order(self, order):
        # logger.info("process the order: ", order)
        # print 'fake message'
        return True

    def reject(self, order):
        pass


