# coding=utf-8


def sh_tax(price, number):
    """
    shanghai stock tax.
    :param price:
    :param number:
    :return:
    """
    return price*number*0.01 + 5


def sz_tax(price, number):
    """
    shenzhen stock tax.
    :param price:
    :param number:
    :return:
    """
    return price*number*0.0005 + 5


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