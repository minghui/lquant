# coding=utf-8
import numpy as np
from report import *
import logbook
import yaml
# from utils.dbutils import DBUtil
import codecs
from algorithm import StrategyBase
from __init__ import *
from algorithm.data.record import Record
from algorithm.data.record_container import RecordContainer
import pandas as pd
from matplotlib import pylab as plt
from backtest.utils.rds import RDSDB

DATA_NEED = {
    "minute": 242,
    "day": 1,
    "5min": 48
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
            self._database = DBUtil(database_config['user'],
                                    str(database_config['passwd']),
                                    database_config['database'])
        elif database_config['name'] == 'rds':
            self._database = RDSDB(self.logger)
            self._db_type = database_config['type']
        self._summary = {}
        self._strategy = None
        # Use to save the everydays return and loss
        self.asset_dict = {}
        self.asset_daliy = []
        self._analysis = None
        self._trade_strategy = None

    def init(self, strategy=None, trade_strategy=None, analysis=None):
        self._strategy = strategy
        self._strategy.set_data_need(DATA_NEED[self._db_type])
        self._analysis = analysis
        self._trade_strategy = trade_strategy

    def set_strategy(self, strategy):
        self._strategy = strategy
        self._strategy.set_data_need(DATA_NEED[self._db_type])

    def test_strategy(self):
        if self._strategy is None:
            raise ValueError("Do not have a strategy")
        for stock in self._backtest_list:
            self._trade_strategy.init(self._fund)
            if self._db_type == 'minute':
                stock_data = self._database.get_daliy_array(stock,
                                                            begin=self._begin_date,
                                                            end=self._end_date,
                                                            m=1)
            elif self._db_type == 'day':
                stock_data = self._database.get_daliy_array(stock,
                                                            begin=self._begin_date,
                                                            end=self._end_date,
                                                            m=1440)
            elif self._db_type == '5minite':
                stock_data = self._database.get_daliy_array(stock,
                                                            begin=self._begin_date,
                                                            end=self._end_date,
                                                            m=5)
            else:
                raise ValueError("Do not support type.")
            # print 'This is the shape of the stock', stock_data.shape
            self._test_strategy(stock, stock_data)

    def summary(self):
        for x in self.asset_dict:
            # print self.asset_dict[x]
            self.get_benchmark()
            asset_return = (self.asset_dict[
                                x] - self._base_fund) / self._base_fund
            asset_return = asset_return.add_prefix(str(x) + "_")
            print asset_return
            result = pd.merge(asset_return, self._benchmark_data,
                              left_index=True, right_index=True, how="inner")
            # print result
            if self._analysis is not None:
                self._analysis(result)
            result.plot()
            plt.show()

    def get_stock_asset(self):
        pass

    def get_benchmark(self):
        """
        Get the benchmark. Used to compare with strategy.
        # """
        # if self._db_type == 'minute':
        #     benchmark_data = self._database.get_array(self._benchmark_name,
        #                                               self._begin_date,
        #                                               self._end_date,
        #                                               m=1)
        # elif self._db_type == 'day':
        benchmark_data = self._database.get_array(self._benchmark_name,
                                                  self._begin_date,
                                                  self._end_date,
                                                  m=1440)
        # elif self._db_type == '5minute':
        #     benchmark_data = self._database.get_array(self._benchmark_name,
        #                                               self._begin_date,
        #                                               self._end_date,
        #                                               m=5)
        # else:
        #     raise ValueError("Do not support type")

        date_index = np.array([x.split(' ')[0] for x in benchmark_data[1:, 0]])
        benchmark_data = benchmark_data[:, 4]
        change_rate = (benchmark_data[1:] - benchmark_data[0]) / benchmark_data[
            0]
        self._benchmark_data = pd.DataFrame(data=change_rate, index=date_index,
                                            columns=["benchmark"])
        print self._benchmark_data

    def _init_assert(self):
        """
        Init the asset.
        """
        self._fund = self._base_fund
        self._strategy.init(self._fund)
        self._trade_strategy.init(self._fund)

    def _test_strategy(self, stock, stock_data):
        # print 'This is the stock_data', stock_data
        needed_data_length = self._strategy.get_data_need()
        for tmp_data in stock_data:
            buy_price = self._strategy.if_buy(tmp_data)
            if buy_price is not None:
                record = self._trade_strategy.buy_strategy(name=stock,
                                                           price=buy_price)
                if record is not None:
                    self._buy_record_list.append(record)
                    self._trade_strategy.get_assert(stock, tmp_data[-1])
                    continue
            sell_price = self._strategy.if_sell(tmp_data)
            if sell_price is not None:
                record = self._trade_strategy.sell_strategy(name=stock,
                                                            price=sell_price)
                if record is not None:
                    self._sell_record_list.append(record)
            self._trade_strategy.get_assert(stock, tmp_data[-1])
        print 'This is stock data', stock_data
        date_index = [x[0] for x in stock_data]
        print stock_data
        print date_index
        result = pd.DataFrame(data=self._trade_strategy.asset_daliy,
                              index=date_index,
                              columns=["return"])
        print result
        self._summary[stock] = self._strategy.summary()
        self.asset_dict.update({stock: result})


class TradeStrategy(object):
    """
    This is t he buy strategy base class.
    """

    def __init__(self):
        self._fund = None
        # for every stock we have a container
        self.stock_asset = RecordContainer()
        self.asset_daliy = None
        self._sell_record_list = []
        self._buy_record_list = []

    def init(self, fund):
        self._fund = fund
        self.stock_asset.clear()
        self.asset_daliy = []

    def buy_strategy(self, *argv, **kwargs):
        """
        Here is just a sample buy strategy.
        :param data:
        :return:
        """
        name = kwargs.get('name')
        price = kwargs.get("price")
        date = kwargs.get("date")
        number = np.floor(self._fund / (price * 100))
        if number != 0:
            self._fund -= price * number * 100
            record = Record(name=name, date=date,
                            number=number, price=price, tax=0, buy=True)
            self.stock_asset.add_record(record)
            return record

    def sell_strategy(self, *args, **kwargs):

        """
        Here is just a sample sell strategy.
        # TODO: Sell strategy should be configable.
        :param data:
        :return:
        """
        name = kwargs.get('name')
        price = kwargs.get("price")
        date = kwargs.get('date')
        record = self.stock_asset.get_record(name)
        if record is not None:
            sell_record = Record(name=name, date=date,
                                 price=price, number=record.number,
                                 tax=0, sell=True)
            self._fund += record.number * price * 100
            self.stock_asset.add_record(sell_record)
            self._sell_record_list.append(sell_record)

    def get_assert(self, stock, data):
        record = self.stock_asset.get_record(stock)
        print record
        if record is not None:
            current_asset = self._fund + record.number * data[4] * 100
        else:
            current_asset = self._fund
        print 'stock', current_asset
        self.asset_daliy.append(current_asset)

    def get_asset_daliy(self):
        return self.asset_daliy


if __name__ == '__main__':
    import yaml
    import codecs

    with codecs.open('./test.yaml', encoding='utf-8') as f:
        data = yaml.load(f)
    print data
