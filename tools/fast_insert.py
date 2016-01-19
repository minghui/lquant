# coding=utf-8
__author__ = 'squall'
import sys
sys.path.append('../')
from backtest.utils.mysql import MySQLUtils
from multiprocessing import Pool
import argparse
from matplotlib import mlab
import os
from itertools import repeat


def insert_data(parameter):
    print parameter[1]
    # for stock in parameter[0]:
    #     data = mlab.csv2rec(stock, delimiter='\t')
    #     parameter[1].insert_data(data, id)


def build_stock_list(data_path):
    stock_list = []
    for root, _, files in os.walk(data_path):
        for f in files:
            stock_list.append(os.path.join(root, f))
    return stock_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='thread number')
    parser.add_argument('-path', type=str, help='path to the data')
    try:
        db = MySQLUtils(user='root', passwd='1988', dbname='test', source='stock')
        args = parser.parse_args()
        stock_list = build_stock_list(args.path)
        length = len(stock_list)/args.n
        stock_cache = [stock_list[i:i+length] for i in range(0, len(stock_list), length)]
        if len(stock_list) % length != 0:
            begin = len(stock_list) / length * length
            stock_cache.append(stock_list[begin:begin + len(stock_list) % length])
        pools = Pool(processes=args.n)
        pools.map(insert_data, zip(stock_cache, repeat(db)))
        pools.close()
        pools.join()
    except Exception as e:
        print e.message
        print 'fuck wrong'