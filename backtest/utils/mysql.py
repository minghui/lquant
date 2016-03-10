# coding=utf-8
# !/usr/bin/env python

"""
insert the stock data to the mysql
"""
import datetime

import MySQLdb
import numpy as np
import pandas as pd

from backtest.utils.dbbase import DBBase
from data.ohlc import OHLCVD


def rec_sql(data, headers=None):
    if headers == None:
        headers = [('date', datetime.date), ('open', float), ('high', float), ('low', float), ('close', float),
                   ('volume', float), ('deal', float)]

    data = np.array(data, dtype=headers)
    data = data.view(np.recarray)
    return data


class MySQLUtils(DBBase):
    """
    This class is used to get data from mysql database, maybe I show use sqlachemy instead.
    """

    def __init__(self, user, passwd, dbname, source):
        DBBase.__init__(self)
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.source = source
        self.db = MySQLdb.connect(user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')
        self.cur = self.db.cursor()
        self._column_name = ["date", "open", "high", "low", "close", "volume", "deal"]
        self._end_date = None
        self._end_date_set = False

    def create_db(self, stock_name):
        # self.stock_name = stock_name
        sql_line = '''
 create table if not exists STOCK(ID VARCHAR(20), DD DATE, START FLOAT, HIGH FLOAT, LOW FLOAT, CLOSE FLOAT, VOLUME FLOAT, DEAL FLOAT)'''
        self.cur.execute(sql_line)
        self.cur.execute("alter table STOCK add unique index(ID, DD)")
        self.db.commit()

    def insert_data(self, data, id):
        if data.shape[0] == 0:
            return None
        sql_line = """INSERT INTO STOCK VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        for d in data:
            try:
                self.cur.execute(sql_line, (id, d[0].__str__(), d[1], d[2], d[3], d[4], np.log(d[5]), np.log(d[6])))
            except MySQLdb.Error as e:
                print e
                print 'already in the database'
        self.db.commit()

    def insert_single_data(self, data):
        '''
        insert one single data into the database
        '''
        sql_line = """INSERT INTO STOCK VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.cur.execute(sql_line, data)
        except MySQLdb.Error as e:
            print e
            print 'already in the database'
        self.db.commit()

    def execute_sql(self, sql_line):
        self.cur.execute(sql_line)
        result = []
        self.db.commit()
        for row in self.cur.fetchall():
            result.append(row)
        return result

    def select_data(self, id, begin=None, end=None, source="STOCK"):
        '''
        begin is the begin time of the stock
        end is the end time of the stock
        '''
        if not isinstance(id, str):
            id = str(id)
        if not (id.startswith('sh') or id.startswith('sz')):
            if id.startswith('6'):
                id = 'sh' + id
            else:
                id = 'sz' + id
        if begin is None:
            sql_line = '''select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL from {source} where ID = '{id}' '''.\
                format(id=id, source=source)
        else:
            sql_line = """select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL from {source} where ID = '{id}' and
 DD >= '{begin}' and DD <= '{end}' """.format(id=id, begin=begin, end=end, source=source)
        print sql_line
        return self.execute_sql(sql_line)

    def get_cur(self):
        return self.cur

    def get_array(self, id, begin=None, end=None, **kwargs):
        result = self.select_data(id, begin=begin, end=end)
        return np.array(result)

    def get_dataframe(self, id, begin=None, end=None):
        result = self.select_data(id, begin=begin, end=end)
        return pd.DataFrame(data=result, columns=self._column_name)

    def get_ohlc(self, id, begin=None, end=None):
        result = self.select_data(id, begin=begin, end=end)
        result = OHLCVD(result)
        return result

    def get_daliy_array(self, id, begin=None, end=None, **kwargs):
        result = self.select_data(id, begin=begin, end=end)

    def get_work_days(self, id, begin=None, end=None, **kwargs):
        result = self.execute_sql("select DISTINCT dd from {source} where dd >='{begin}' and dd <= '{end}'".format(
            source=self.source,
            begin=begin,
            end=end))
        result = [x[0] for x in result]
        return result

    def set_end_date(self, end_date):
        self._end_date = end_date
        self._end_date_set = True

    def select_data_by_number(self, id, number, end_date):
        """
        Select data by number.
        :param number:
        :param end_date:
        :return:
        """
        sql_str = """ select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL from
 {source} where id = '{id}' and dd <= '{end_date}' order by
dd desc limit {number}""".format(source=self.source, end_date=end_date,
                                 number=number, id=id)
        print sql_str
        data = self.execute_sql(sql_str)
        return np.array(data)

    def select_data_by_date(self, begin_date, end_date):
        """
        Select data by begin_date and end date.
        :param begin_date:
        :param end_date:
        :return:
        """
        sql_str = """ select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL
  from {source} where dd >= {begin_date} and
 dd <= {end_date}""".format(source=self.source, begin_date=begin_date,
                              end_date=end_date)
        data = self.execute_sql(sql_str)
        return data

if __name__ == '__main__':
    stock_db = MySQLUtils('root', '1988', 'test', 'stock')
    result = stock_db.select_data('sh600741', begin='2015-10-10', end='2015-11-11')
    print result
    result_time = [str(x[0]) for x in result]
    print result_time
    #stock_name = stock_list('e:/stock-10-16/')
    # stock_db.create_db('STOCK')
    # for root, _, files in os.walk('./data/'):
    #     for f in files:
    #         id = f[:-4]
    #         id = id.lower()
    #         print id
    #         data = mlab.csv2rec(os.path.join(root, f), delimiter='\t')
    #         stock_db.insert_data(data, id)
            #for stock in stock_name:
            #    print stock
            #    stock_db.select_data(stock)



