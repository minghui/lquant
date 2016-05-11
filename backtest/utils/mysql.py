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
        headers = [('date', datetime.date), ('open', float), ('high', float),
                   ('low', float), ('close', float),
                   ('volume', float), ('deal', float)]

    data = np.array(data, dtype=headers)
    data = data.view(np.recarray)
    return data


class MySQLUtils(DBBase):
    """
    This class is used to get data from mysql database, maybe I show use
    sqlachemy instead.
    """

    def __init__(self, user, passwd, dbname, source):
        DBBase.__init__(self)
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.source = source
        self.db = MySQLdb.connect(user=self.user, passwd=self.passwd,
                                  db=self.dbname, charset='utf8')
        self.cur = self.db.cursor()
        self._column_name = ["date", "open", "high", "low", "close", "volume",
                             "deal"]
        self._end_date = None
        self._end_date_set = False

    def create_ohlc_db(self, stock_name):
        # self.stock_name = stock_name
        sql_line = '''
 create table if not exists STOCK(ID VARCHAR(20), DD DATE, START FLOAT,
  HIGH FLOAT, LOW FLOAT, CLOSE FLOAT, VOLUME FLOAT, DEAL FLOAT)'''
        self.cur.execute(sql_line)
        self.cur.execute("alter table STOCK add unique index(ID, DD)")
        self.db.commit()

    def create_feature_db(self, database_name):
        sql_line = """
        DROP TABLE IF EXISTS {dababase_name};
CREATE TABLE IF NOT EXISTS {database_name}(
     ID VARCHAR(20),
  DD DATE,
  START FLOAT,
  HIGH FLOAT,
   LOW FLOAT,
   CLOSE FLOAT,
   VOLUME FLOAT,
   DEAL FLOAT,
    ATR FLOAT,
    NATR FLOAT,
    TRANGE FLOAT,
    DEMA FLOAT,
    EMA FLOAT,
    HT_TRENDLINE FLOAT,
    KAMA FLOAT,
    MA FLOAT,
    MIDPOINT FLOAT,
    MIDPRICE FLOAT,
    SAR FLOAT,
    SAREXT FLOAT,
    SMA FLOAT,
    T3 FLOAT,
    TEMA FLOAT,
    TRIMA FLOAT,
    WMA FLOAT,
    BETA FLOAT,
    CORREL FLOAT,
    LINEARREG FLOAT,
    LINEARREG_ANGLE FLOAT,
    LINEARREG_INTERCEPT FLOAT,
    LINEARREG_SLOPE FLOAT,
    STDDEV FLOAT,
    TSF FLOAT,
    VAR FLOAT,
    ADX FLOAT,
    ADXR FLOAT,
    APO FLOAT,
    AROONOSC FLOAT,
    BOP FLOAT,
    CCI FLOAT,
    CMO FLOAT,
    DX FLOAT,
    MFI FLOAT,
    MINUS_DI FLOAT,
    MINUS_DM FLOAT,
    MOM FLOAT,
    PLUS_DI FLOAT,
    PLUS_DM FLOAT,
    PPO FLOAT,
    ROC FLOAT,
    ROCP FLOAT,
    ROCR FLOAT,
    ROCR100 FLOAT,
    RSI FLOAT,
    TRIX FLOAT,
    ULTOSC FLOAT,
    WILLR FLOAT,
    CDL2CROWS FLOAT,
    CDL3BLACKCROWS FLOAT,
    CDL3INSIDE FLOAT,
    CDL3LINESTRIKE FLOAT,
    CDL3OUTSIDE FLOAT,
    CDL3STARSINSOUTH FLOAT,
    CDL3WHITESOLDIERS FLOAT,
    CDLABANDONEDBABY FLOAT,
    CDLADVANCEBLOCK FLOAT,
    CDLBELTHOLD FLOAT,
    CDLBREAKAWAY FLOAT,
    CDLCLOSINGMARUBOZU FLOAT,
    CDLCONCEALBABYSWALL FLOAT,
    CDLCOUNTERATTACK FLOAT,
    CDLDARKCLOUDCOVER FLOAT,
    CDLDOJI FLOAT,
    CDLDOJISTAR FLOAT,
    CDLDRAGONFLYDOJI FLOAT,
    CDLENGULFING FLOAT,
    CDLEVENINGDOJISTAR FLOAT,
    CDLEVENINGSTAR FLOAT,
    CDLGAPSIDESIDEWHITE FLOAT,
    CDLGRAVESTONEDOJI FLOAT,
    CDLHAMMER FLOAT,
    CDLHANGINGMAN FLOAT,
    CDLHARAMI FLOAT,
    CDLHARAMICROSS FLOAT,
    CDLHIGHWAVE FLOAT,
    CDLHIKKAKE FLOAT,
    CDLHIKKAKEMOD FLOAT,
    CDLHOMINGPIGEON FLOAT,
    CDLIDENTICAL3CROWS FLOAT,
    CDLINNECK FLOAT,
    CDLINVERTEDHAMMER FLOAT,
    CDLKICKING FLOAT,
    CDLKICKINGBYLENGTH FLOAT,
    CDLLADDERBOTTOM FLOAT,
    CDLLONGLEGGEDDOJI FLOAT,
    CDLLONGLINE FLOAT,
    CDLMARUBOZU FLOAT,
    CDLMATCHINGLOW FLOAT,
    CDLMATHOLD FLOAT,
    CDLMORNINGDOJISTAR FLOAT,
    CDLMORNINGSTAR FLOAT,
    CDLONNECK FLOAT,
    CDLPIERCING FLOAT,
    CDLRICKSHAWMAN FLOAT,
    CDLRISEFALL3METHODS FLOAT,
    CDLSEPARATINGLINES FLOAT,
    CDLSHOOTINGSTAR FLOAT,
    CDLSHORTLINE FLOAT,
    CDLSPINNINGTOP FLOAT,
    CDLSTALLEDPATTERN FLOAT,
    CDLSTICKSANDWICH FLOAT,
    CDLTAKURI FLOAT,
    CDLTASUKIGAP FLOAT,
    CDLTHRUSTING FLOAT,
    CDLTRISTAR FLOAT,
    CDLUNIQUE3RIVER FLOAT,
    CDLUPSIDEGAP2CROWS FLOAT,
    CDLXSIDEGAP3METHODS FLOAT,
    AD FLOAT,
    ADOSC FLOAT,
    OBV FLOAT,
    MAX FLOAT,
    MAXINDEX FLOAT,
    MIN FLOAT,
    MININDEX FLOAT,
    MULT FLOAT,
    SUB FLOAT,
    SUM FLOAT,
    ACOS FLOAT,
    ASIN FLOAT,
    ATAN FLOAT,
    CEIL FLOAT,
    COS FLOAT,
    COSH FLOAT,
    EXP FLOAT,
    FLOOR FLOAT,
    LN FLOAT,
    LOG10 FLOAT,
    SIN FLOAT,
    SINH FLOAT,
    SQRT FLOAT,
    TAN FLOAT,
    TANH FLOAT,
    AVGPRICE FLOAT,
    MEDPRICE FLOAT,
    TYPPRICE FLOAT,
    WCLPRICE FLOAT,
    HT_DCPERIOD FLOAT,
    HT_DCPHASE FLOAT,
    HT_TRENDMODE FLOAT
)
        """.format(database_name=database_name)
        self.cur.execute(sql_line)
        self.cur.execute("alter table {source} add unique index(ID, DD)".format(source=database_name))
        self.db.commit()

    def insert_ohlc_data(self, data, id):
        if data.shape[0] == 0:
            return None
        sql_line = """INSERT INTO STOCK VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        for d in data:
            try:
                self.cur.execute(sql_line, (id, d[0].__str__(), d[1],
                                            d[2], d[3], d[4], np.log(d[5]),
                                            np.log(d[6])))
            except MySQLdb.Error as e:
                pass
                # print e
                # print 'already in the database'
        self.db.commit()

    def insert_feature_data(self, data, id):
        if isinstance(data, np.ndarray):
            pass
        if isinstance(data, pd.DataFrame):
            data = data.values
        if data.shape[0] == 0:
            return None

        sql_line = '''insert into stock_with_feature values('{id}', '{date}', {data} )'''
        for d in data:
            try:
                data_str = ','.join(data[1:])
                line = sql_line.format(id=id, date=d[0], data=data_str)
                self.cur.execute(line)
            except MySQLdb.Error as e:
                pass

    def insert_single_data(self, data):
        '''
        insert one single data into the database
        '''
        sql_line = """INSERT INTO STOCK VALUES(%s, %s, %s, %s, %s,
 %s, %s, %s)"""
        try:
            self.cur.execute(sql_line, data)
        except MySQLdb.Error as e:
            pass
            # print e
            # print 'already in the database'
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
            sql_line = '''select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL from
{source} where ID = '{id}' '''. \
                format(id=id, source=source)
        else:
            sql_line = """select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL
from {source} where ID = '{id}' and
 DD >= '{begin}' and DD <= '{end}'
 """.format(id=id, begin=begin, end=end, source=source)
        # print sql_line
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
        result = self.execute_sql("""select DISTINCT dd from {source} where
id = '{id}' and dd >='{begin}' and dd <= '{end}'""".format(
            source=self.source,
            begin=begin,
            end=end,
            id=id))
        result = [x[0] for x in result]
        return result

    def set_end_date(self, end_date):
        self._end_date = end_date
        self._end_date_set = True

    def select_data_by_number(self, id, number, end_date, reversed=True):
        """
        Select data by number.
        :type reversed: bool
        :param number:
        :param end_date:
        :return:
        """
        sql_str = """ select DD, START, HIGH, LOW, CLOSE, VOLUME, DEAL from
 {source} where id = '{id}' and dd <= '{end_date}' order by
dd desc limit {number}""".format(source=self.source, end_date=end_date,
                                 number=number, id=id)
        # print sql_str
        data = self.execute_sql(sql_str)
        if reversed:
            data = data[::-1]
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

    def select_current_price(self, date):
        pass

    def get_all_stock(self):
        sql_str = """
        select DISTINCT id FROM {source}
        """.format(source=self.source)
        data = self.execute_sql(sql_str)
        data = [x[0] for x in data]
        return data


if __name__ == '__main__':
    stock_db = MySQLUtils('root', '1988', 'test', 'stock')
    result = stock_db.select_data('sh600741', begin='2015-10-10',
                                  end='2015-11-11')
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



