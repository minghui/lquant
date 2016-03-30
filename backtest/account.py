# coding=utf-8

from Configurable import Configurable
from backtest.order_book import OrderBook
from data.order import Order
import numpy as np
import logging
from backtest.utils.utils import get_module_logger


logger = get_module_logger(__name__)
logger.info("init the loger from " + __name__)


class Account(Configurable):
    """
    This is the core class in the simulator, since account is the center of
    my framework, it connect the market and the algorithm(which is human in
    general). So this class must be well designed.
    """
    def set_to_context(self, context):
        pass

    def get_from_context(self, context):
        pass

    def __init__(self, cash, database):
        """
        In order to simualte the T+1 market, in this class, I have added the
        old order and the new order variable. The new order is the order deal
        today, so it can not sell immediately. After every day, new order and
        the old order will be combine together, and the new order will be empty.
        :param cash:
        :param database:
        :return:
        """
        self._cash = cash
        self._stock_asset = {}
        self._order_book = OrderBook()
        self._new_order = {}
        self._old_order = {}
        # Account should have ability to connect the database.
        self._dbbase = database

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        self._cash = cash

    def init_from_config(self, config, **kwargs):
        """
        Read config from the main config file.
        :param config:
        :param kwargs:
        :return:
        """
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
            self._cash = self._cash-order.buy_price*order.number*100
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
            # clean the stock
            if self._stock_asset[order.name].number == 0:
                del self._stock_asset[order.name]
            self._old_order[order.name] += order
            if self._old_order[order.name].number == 0:
                del self._old_order[order.name]

            self._cash += order.buy_price*order.number*100
            return True
        else:
            return False

    def _before_market(self, date):
        """
        process the data before the market open.
        :param date:
        :return:
        """
        return None

    def _after_market(self, date):
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
        """
        Get every stock asset's return, may be I should remove this method.
        :param date:
        :return:
        """
        for name in self._old_order:
            try:
                # print name, date
                logger.debug("name is {name}, date is {date}".format(name=name,
                                                                     date=date))
                data = self._dbbase.get_dataframe(name, begin=date, end=date)
                close_price = data.close.values[-1]
                self._old_order[name].current_price = close_price
                self._old_order[name].return_rate = (self._old_order[name]
                                                     .current_price
                                                     - self._old_order[name]
                                                     .buy_price/self
                                                     ._old_order[name].buy_price
                                                     )
            except Exception as e:
                logger.exception(e.message)
                print e.message
                print 'error at date:', date, ' name:', name

    def get_stock_asset(self):
        return self._old_order

    def create_buy_order(self, name, price, context, position=1.0):
        """
        This function is used to create buy order by some parameter.
        :param name:
        :param price:
        :param tax_processor:
        :param position:
        :return:
        """
        logger.info("create buy order at time {date}".format(date=context.date))
        used_cash = self._cash * position
        buy_price = context.tax_processor.calculate_buy_tax(price)
        number = np.floor(used_cash/(buy_price*100))
        order = Order(name=name, price=buy_price, date=context.date,
                      number=number,
                      current_price=price,
                      buy=True)
        return order

    def create_sell_order(self, name, price, context, position=1.0):
        """
        This function is used to create sell order by some parameter.
        :param name:
        :param price:
        :param date:
        :param tax_processor:
        :param position:
        :return:
        """
        if name not in self._old_order[name]:
            raise ValueError('Stock not in the order list')
        order = self._old_order[name]
        sell_price = context.tax_processor_calculate_sell_tax(price)
        sell_number = np.floor(order.number*position)
        return Order(name=name, price=sell_price,
                     current_price=price,
                     date=context.date,
                     number=sell_number, sell=True)

    def get_cash(self):
        """
        get money we have.
        :return:
        """
        total_cash = self._cash
        for key in self._stock_asset:
            asset = self._stock_asset[key]
            total_cash += asset.current_price*asset.number*100
        return total_cash

if __name__ == "__main__":
    pass