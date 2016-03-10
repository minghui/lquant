# coding=utf-8
from backtest.account import Account


class Context(object):
    """
    This class is used to save the result.
    """

    def __init__(self):
        self.account = None
        self.db = None
        self.date = None
        self.asset_code = None


if __name__ == "__main__":
    context = Context()
    context.account = Account(1000)