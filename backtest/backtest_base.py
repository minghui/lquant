# coding=utf-8
import numpy as np
from report import *
import logbook
import yaml
try:
    from utils.mysql import MySQLUtils
except:
    print 'Can not import Mysql'
import codecs
from __init__ import *
import pandas as pd
from matplotlib import pylab as plt
from backtest.utils.rds import RDSDB
from datetime import datetime, timedelta


DATA_NEED = {
    "minute": 242,
    "day": 1,
    "5min": 48
}

M_TYOE = {
    "day": 1440,
    "minute": 1,
    "5min": 240
}


class BackTestBase(object):
    '''
    Get a strategy, test if this strategy work in some perodic.
    '''

    def __init__(self, config_file=None, *args, **kwargs):
        self.logger = kwargs.get('log')
        self._buy_record_list = []
        self._sell_record_list = []
        with codecs.open(config_file, encoding='utf-8') as f:
            config = yaml.load(f)
        if config is None:
            raise ValueError("Need config file")
        with codecs.open(config_file, encoding='utf-8') as f:
            config = yaml.load(f)
        if isinstance(config['test_list'], list):
            self._backtest_list = config['test_list']
        else:
            self._backtest_list = ALL_STOCK_LIST
        self._fund = config['fund']
        self._base_fund = self._fund
        self._begin_date = config['begin']
        self._end_date = config['end']
        # Compare with
        self._benchmark_name = config['benchmark']
        self._benchmark_data = None
        # Use database to store data.
        database_config = config['database']
        if database_config['name'] == 'mysql':
            self._database = MySQLUtils(database_config['user'],
                                        str(database_config['passwd']),
                                        database_config['database'],
                                        database_config['source'])
        elif database_config['name'] == 'rds':
            self._database = RDSDB(self.logger)
        else:
            raise ValueError("Do not support data source")
        self._qury_type = config['query_type']
        self._need_data_length = config['need_data_length']
        self._summary = {}
        self._strategy = None
        # Use to save the everydays return and loss
        self.asset_dict = {}
        self.asset_daliy = []
        self._analysis = None
        self._trade_strategy = None
        self._date_type = config['date_type']
        self._tax = config["tax"]

    def init(self, strategy=None, trade_strategy=None, analysis=None):
        """
        Init the strategy , trade_strategy and analysis function.
        :param strategy: Chceck if buy or is sell.
        :param trade_strategy:  Buy or sell.
        :param analysis:  Analysis the result.
        :return:
        """
        self._strategy = strategy
        self._analysis = analysis
        self._trade_strategy = trade_strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def set_trade_strategy(self, trade_strategy):
        self._trade_strategy = trade_strategy

    def test_strategy(self):
        """
        This is the main function of the backtest.
        Is used to start the backtest.
        :return:
        """
        if self._strategy is None or self._trade_strategy is None:
            raise ValueError("Do not have a strategy")
        for stock in self._backtest_list:
            self._trade_strategy.init(self._fund)
            work_days = self._database.get_work_days(stock, begin=self._begin_date, end=self._end_date)
            for day in work_days:
                day = datetime.strptime(str(day), self._date_type)
                if self._need_data_length.endswith('days'):
                    data_len = int(self._need_data_length.split('days')[0])
                    begin = datetime.strftime(day-timedelta(data_len-1), self._date_type)
                    end = datetime.strftime(day+timedelta(1), self._date_type)
                else:
                    raise ValueError("Do not supoort data length")
                m_type = M_TYOE[self._qury_type]
                stock_data = self._database.get_array(stock, begin=begin, end=end, m=m_type)
                self._test_strategy(stock, stock_data=stock_data)
                self._trade_strategy.get_asset(stock, stock_data[-1])
                # print 'This is stock data', stock_data
            # print stock_data
            # print 'This is date index', date_index
            date_index = [datetime.strptime(str(x), self._date_type) for x in work_days]
            result = pd.DataFrame(data=self._trade_strategy.asset_daliy,
                                  index=date_index,
                                  columns=["return"])
            self._summary[stock] = self._strategy.summary()
            max_withdraw = self.get_max_withdraw(stock, begin=self._begin_date, end=self._end_date)
            self.asset_dict.update({stock:
                                        {
                                            "return": result,
                                            "max_withdraw": max_withdraw
                                         }})
        self.summary()

    def summary(self):
        """
        This function is used to summary the result.
        If you want calculate some other indicator, you can add them here.
        :return:
        """
        if self._analysis is not None:
            self._analysis(self.asset_dict)
        # for x in self.asset_dict:
        #     self.get_benchmark()
        #     asset_return = (self.asset_dict[x] - self._base_fund) / self._base_fund
        #     asset_return = asset_return.add_prefix(str(x) + "_")
        #     print asset_return
        #     result = pd.merge(asset_return, self._benchmark_data,
        #                       left_index=True, right_index=True, how="inner")
        #     max_return = self.get_max_return(x, begin=self._begin_date, end=self._end_date)
        #     print max_return
        #     # print result
        #     # if self._analysis is not None:
        #     #     self._analysis(result)
        #     # result.plot()
        #     # plt.show()

    def get_benchmark(self):
        """
        Get the benchmark. Used to compare with strategy.
        """

        benchmark_data = self._database.get_array(self._benchmark_name,
                                                  self._begin_date,
                                                  self._end_date,
                                                  m=1440)

        date_index = np.array([x.split(' ')[0] for x in benchmark_data[1:, 0]])
        benchmark_data = benchmark_data[:, 4]
        change_rate = (benchmark_data[1:] - benchmark_data[0]) / benchmark_data[
            0]
        self._benchmark_data = pd.DataFrame(data=change_rate, index=date_index,
                                            columns=["benchmark"])
        print self._benchmark_data

    def get_max_withdraw(self, stock, begin=None, end=None):
        """
        Calculate the max return.
        """
        day_data = self._database.get_array(stock, begin=begin, end=end, m=1440)
        day_data = day_data[:, 4]
        max_loc = np.argmax(day_data)
        after_data = day_data[max_loc:]
        min_loc = np.argmin(after_data)
        min_price = after_data[min_loc]
        max_return = (day_data[max_loc] - min_price)/day_data[min_loc] * 100
        return max_return

    def _init_assert(self):
        """
        Init the asset.
        """
        self._fund = self._base_fund
        self._strategy.init(self._fund)
        self._trade_strategy.init(self._fund)

    def _test_strategy(self, stock, stock_data):
        """
        Test strategy.
        :param stock:
        :param stock_data:
        :return:
        """
        # print 'This is the stock_data', stock_data
        buy_detail = self._strategy.if_buy(stock_data)
        if buy_detail is not None:
            result = self._trade_strategy.buy_strategy(name=stock,
                                                       price=buy_detail[0],
                                                       date=buy_detail[1],
                                                       tax=self._tax,
                                                       buy=True)
            if result:
                return
        sell_detail = self._strategy.if_sell(stock_data)
        if sell_detail is not None:
            self._trade_strategy.sell_strategy(name=stock,
                                               price=sell_detail[0],
                                               date=sell_detail[1],
                                               tax=self._tax,
                                               sell=True)

if __name__ == '__main__':
    import yaml
    import codecs
    with codecs.open('./test.yaml', encoding='utf-8') as f:
        data = yaml.load(f)
    print data
