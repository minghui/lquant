# coding=utf-8
#!/usr/bin/python

import numpy as np


def calculate_return(order):
    profit = (order.current_price - order.cost)*order.number
    profit_rate = profit / order.cost*order.number

    return (profit, profit_rate)

