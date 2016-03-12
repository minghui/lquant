# coding=utf-8

from Configurable import Configurable
from backtest.order_book import OrderBook
from data.order import Order
import numpy as np


class Account(Configurable):

    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def __init__(self, cash, database):
        self._cash = cash
        self._stock_asset = {}
        self._order_book = OrderBook()
        self._new_order = {}
        self._old_order = {}
        self._dbbase = database

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        self._cash = cash

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
        if order.buy_price*order.number > self._cash:
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
            self._cash = self._cash - order.buy_price*order.number*100
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
        print "This is order name :", order.name
        print self._old_order
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
            self._cash += order.buy_price*order.number*100
            return True
        else:
            return False

    def after_market(self, date):
        """
        Process the data after the market close.
        :param date: type str
        :return:
        """
        for key in self._stock_asset:
            data = self._dbbase.get_dataframe(key, begin=date, end=date)
            self._stock_asset[key].current_price = data.close.values[-1]
        # Combine the old_order and new_order
        for name in self._new_order:
            if name in self._old_order:
                self._old_order[name] += self._new_order[name]
            else:
                self._old_order[name] = self._new_order[name]
            self._new_order = {}
        self._update_asset(date)

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
            data = self._dbbase.get_dataframe(stock_asset.name, begin=date,
                                              end=date)
            stock_asset.current_price = data.close.values[-1]

    def get_return(self, date):
        for name in self._old_order:
            data = self._dbbase.get_dataframe(name, begin=date, end=date)
            close_price = data.close.values[-1]
            self._old_order[name].current_price = close_price
            self._old_order[name].return_rate = (self._old_order[name].current_price
                                                 - self._old_order[name].buy_price)/\
                                                self._old_order[name].buy_price

    def get_stock_asset(self):
        return self._old_order

    def create_buy_order(self, name, price, date, tax_processor, position=1.0):
        """
        This function is used to create buy order by some parameter.
        :param name:
        :param price:
        :param tax_processor:
        :param position:
        :return:
        """

        used_cash = self._cash * position
        buy_price = tax_processor.calculate_tax(price, used_cash)
        number = np.floor(used_cash/buy_price)
        order = Order(name=name, price=buy_price, date=date, number=number,
                      buy=True)
        return order

    def create_sell_order(self, name, price, date, tax_processor, position=1.0):
        """
        This function is used to create sell order by some parameter.
        :param name:
        :param price:
        :param date:
        :param tax_processor:
        :param position:
        :return:
        """
        raise Exception('Unimplement Error')

if __name__ == "__main__":
    pass