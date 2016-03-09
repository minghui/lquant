# coding=utf-8

from Configurable import Configurable
from backtest.order_book import OrderBook


class Account(Configurable):

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def __init__(self, cash):
        self._cash = cash
        self._stock_asset = {}
        self._order_book = OrderBook()
        self._new_order = {}
        self._old_order = {}

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
            # Add order to the asset.
            if order.name in self._stock_asset:
                self._stock_asset[order.name] += order
            else:
                self._stock_asset[order.name] = order
            # Add order to the new order.
            if order.name in self._new_order:
                self._new_order[order.name] += order
            else:
                self._new_order[order.name] = order
        else:
            return False

    def sell(self, order, market=None):
        """
        Sell order, there are some other process method should add.
        :param order:
        :param market:
        :return:
        """
        if market is None:
            raise ValueError("Invalid market")

        # Check if order in the old order
        if order.name not in self._old_order:
            raise ValueError("Do not have such stock asset")
        if order.number > self._old_order[order.name].number:
            raise ValueError("Can not sell too much")

        # Flash the order in the old order and the stock asset.
        if market.process_order(order):
            self._order_book.add_order(order)
            self._stock_asset[order.name] += order
            self._old_order[order.name] += order
            return True
        else:
            return False

    def _after_market(self, date):
        """
        Process the data after the market close.
        :param date: type str
        :return:
        """
        for key in self._stock_asset:
            current_price = self._dbbase.get(key, date)
            self._stock_asset[key].current_price = current_price
        # Combine the old_order and new_order
        for name in self._new_order:
            if name in self._old_order:
                self._old_order[name] += self._new_order[name]
            else:
                self._old_order[name] = self._new_order[name]
            self._new_order = {}

    def _before_market(self, date):
        """
        process the data before the market open.
        :param date:
        :return:
        """
        return None

    def _update_asset(self, date):
        """
        Update the asset result.
        :param date:
        :return:
        """
        for key in self._stock_asset:
            stock_asset = self._stock_asset[key]
            data = self._dbbase.get(stock_asset.name, date)
            stock_asset.current_price = data


if __name__ == "__main__":
    pass