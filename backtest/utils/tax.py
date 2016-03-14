# coding=utf-8
import numpy as np


def sh_tax(price, number, tax):
    """
    shanghai stock tax.
    :param price:
    :param number:
    :return:
    """
    return price*number*tax


def sz_tax(price, number, tax):
    """
    shenzhen stock tax.
    :param price:
    :param number:
    :return:
    """
    return price*number*tax


def buy_tax(price, number, market):
    """
    Calculate tax.
    :param price:
    :param number:
    :param market:
    :return:
    """
    if market == 'sh':
        return sh_tax(price, number)
    else:
        return sz_tax(price, number)


def max_buy_number(fund, price, tax):
    price = price + price*tax
    number = np.floor(fund/(price*100))
    return number


class TaxProcessor(object):
    key_this = "tax"
    key_buy_stamp_tax = "buy_stamp_tax"
    key_buy_broker_tax = "buy_broker_tax"
    key_sell_stamp_tax = "sell_stamp_tax"
    key_sell_broker_tax = "sell_broker_tax"

    def __init__(self):
        self._buy_stamp_tax = None
        self._buy_broker_tax = None
        self._sell_stamp_tax = None
        self._sell_broker_tax = None

    def init_from_config(self, config):
        if self.key_this in config:
            this_config = config[self.key_this]
            self._buy_stamp_tax = this_config[self.key_buy_stamp_tax]
            self._buy_broker_tax = this_config[self.key_buy_broker_tax]
            self._sell_stamp_tax = this_config[self.key_sell_stamp_tax]
            self._sell_broker_tax = this_config[self.key_sell_broker_tax]
        else:
            raise ValueError("Do not has {key} key".format(key=self.key_this))

    def calculate_buy_tax(self, price):
        """
        Calculate the price with tax.
        :param price:
        :return:
        """
        return price*(1+self._broker_tax+self._stamp_tax)

    def calculate_sell_tax(self, price):
        """
        Calculate sell tax. Not that sample.
        :param price:
        :return:
        """
        return price
