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
