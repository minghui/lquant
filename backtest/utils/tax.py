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