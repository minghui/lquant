# coding=utf-8
# !/usr/bin/env python

"""
insert the stock data to the mysql
"""
import MySQLdb
import numpy as np
import pandas as pd
import datetime
from .dbbase import DBBase
from .ohlc import OHLCVD

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

    def __init__(self, user, passwd, dbname):
        DBBase.__init__(self)
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.db = MySQLdb.connect(user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')
        self.cur = self.db.cursor()

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
        if begin is None:
            sql_line = '''select DD, OPEN, HIGH, LOW, CLOSE, VOLUME, DEAL from {source} where ID = '{id}' '''.format(id=id, source=source)
        else:
            sql_line = """select DD, OPEN, HIGH, LOW, CLOSE, VOLUME, DEAL from {source} where ID = '{id}' and
 DD >= '{begin}' and DD <= '{end}' """.format(id=id, begin=begin, end=end, source=source)
        print sql_line
        return self.execute_sql(sql_line)

    def get_cur(self):
        return self.cur

    def get_array(self, id, begin=None, end=None):
        result = self.select_data(id, begin=begin, end=end)
        return np.array(result)

    def get_dataframe(self, id, begin=None, end=None):
        result = self.select_data(id, begin=begin, end=end)
        return pd.DataFrame(data=result, columns=self._column_name)

    def get_ohlc(self, id, begin=None, end=None):
        result = self.select_data(id, begin=begin, end=end)
        result = OHLCVD(result)
        return result

if __name__ == '__main__':
    stock_db = MySQLUtils('root', '1988', 'test')
    result = stock_db.select_data('sh600741', begin='2015-10-10', end='2015-11-11')
    print result
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



