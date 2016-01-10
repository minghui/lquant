# coding=utf-8


import pandas as pd
import datetime
from backtest.utils.dbbase import DBBase


class RDSDB(DBBase):
    def __init__(self, logger):
        # http://114.215.202.25:8082/stockBar?code=600000&ex=sh&start=20150306&end=20150407&m=1440
        self.ip = "114.215.202.25"
        self.port = 8082
        self.format = "http://%s:%d/stockBar?code=%s&ex=%s&start=%s&end=%s&m=%s"
        self.df = None
        self.logger = logger

        self.ex = None
        self.code = None

    def store(self, fileName):
        self.df.to_csv(fileName, encoding='utf-8', index=False)

    def get_dataframe(self, code="600000", start=20150101, end=20150130, m=1440):
        self.df = None
        self.code = code
        requestURL = self.format % (self.ip, self.port, code, "", start, end, m)
        self.logger.info(requestURL)

        try:
            self.df = pd.read_csv(requestURL)
        except Exception, e:
            self.df = None
            self.logger.info(requestURL + e.message)

            return False
        if self.df is None:
            return False
        if 'time' not in self.df.columns:
            return False
        if len(self.df.time.values) == 0:
            return False

        self.days = []
        self.times = []
        self._process_sorted_uniq_date()
        self.df['date'] = self.days
        self.df.set_index(['date'])
        self.df['datetime'] = self.times

        self.df.set_index('date')
        return True

    def get_sorted_uniq_date(self):
        if self.days is None:
            raise ValueError("get_sorted_uniq_date")
        return self.days

    def _process_sorted_uniq_date(self):
        date = self.df['time']
        self.dict_days = {}
        date.apply(self._process_time)
        arrayDates = sorted(self.dict_days)
        return arrayDates

    def _process_time(self, x):
        t = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M")
        self.times.append(t)
        day = int(t.strftime("%Y%m%d"))
        self.days.append(day)

    def get_row(self, day):
        row = self.df[self.df.date == day]
        return row

    def get_array(self, id, begin=None, end=None, **kwargs):
        if 'm' in kwargs:
            m = kwargs.get('m')
            result = self.get_dataframe(code=id, start=begin, end=end, m=m)
            if result:
                return self.df.values
            else:
                return None
        return None

    def get_daliy_array(self, id, begin=None, end=None, **kwargs):
        self.result = []
        m = kwargs.get('m')
        date_index = pd.date_range(start=str(begin), end=str(end))
        for x in date_index:
            request_time = datetime.datetime.strftime(x, '%Y%m%d')
            data = self.get_dataframe(code=id, start=request_time,
                                      end=request_time,
                                      m=m)
            print data
            if data:
                self.result.append(self.df.values)
        return self.result

    def get_work_days(self, id, begin=None, end=None):
        self.get_dataframe(id, start=begin, end=end, m=1440)
        return self.get_sorted_uniq_date()


if __name__ == "__main__":
    import os
    import logging

    home_dir = "./"
    if not os.path.exists(os.path.join(home_dir, "log")):
        os.mkdir(os.path.join(home_dir, "log"))

    logging.basicConfig(level=logging.NOTSET,
                        format='%(asctime)s %(name)-12s '
                               '%(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=os.path.join(home_dir, 'RdsInterface.log'),
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    stock = RDSDB(logging)
    ex = "SH"
    code = "600741"
    result = stock.get_array(code, begin='20150101', end='20151220', m=1440)
    print result[:, 4]
