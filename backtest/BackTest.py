# coding=utf-8
import numpy as np
from report import *
import logbook
import yaml
from utils.dbutils import DBUtil
import codecs
from algorithm import StrategyBase
from __init__ import *
from algorithm.data.record import Record
from algorithm.data.record_container import RecordContainer
import pandas as pd
from matplotlib import pylab as plt


class BackTestBase(object):
    '''
    Get a strategy, test if this strategy work in some perodic.
    '''

    def __init__(self, config_file=None, *args, **kwargs):
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
        # Use database to store data.

        self._database = DBUtil(config['user'], str(config['passwd']), config['database'])
        self._summary = {}
        self._strategy = None
        # for every stock we have a container
        self.stock_asset = RecordContainer()
        # Use to save the everydays return and loss
        self.asset_dict = {}

    def buy_strategy(self, name, data):
        """
        Here is just a sample buy strategy.
        :param data:
        :return:
        """
        number = np.floor(self._fund/(data[4]*100))
        if number != 0:
            record = Record(name=name, date=data[1],
                            number=number, price=data[4], tax=0, buy=True)
            self.stock_asset.add_record(record)
            return record

    def sell_strategy(self, name, data):
        """
        Here is just a sample sell strategy.
        # TODO: Sell strategy should be configable.
        :param data:
        :return:
        """
        record = self.stock_asset.get_record(name)
        sell_record = Record(name=name, date=data[1],
                             price=data[4], number=record.number, tax=0, sell=True)
        self._fund += record.number*data[4]
        self.stock_asset.add_record(sell_record)
        self._sell_record_list.append(sell_record)

    def set_strategy(self, strategy):
        self._strategy = strategy

    def test_strategy(self):
        if self._strategy is None:
            raise ValueError("Do not have a strategy")
        for stock in self._backtest_list:
            self.stock_asset.clear()
            self._fund = self._base_fund
            self._strategy.init(self._fund)
            stock_data = self._database.get_array(stock, self._begin_date, self._end_date)

            self._test_strategy(stock, stock_data)

    def _test_strategy(self, stock, stock_data):
        needed_data_length = self._strategy.get_data_need()
        asset_daliy = []
        for i in range(needed_data_length, stock_data.shape[0]):
            tmp_data = stock_data[(i-needed_data_length):i]
            if_buy = self._strategy.if_buy(tmp_data[-1])
            if if_buy:
                record = self.buy_strategy(stock, tmp_data[-1])
                self._buy_record_list.append(record)
            if_sell = self._strategy.if_sell(tmp_data[-1])
            if if_sell:
                record = self.sell_strategy(stock, tmp_data[-1])
                self._sell_record_list.append(record)
            record = self.stock_asset.get_record(stock)
            current_asset = self._fund + record.number*tmp_data[-1, 4]
            asset_daliy.append(current_asset)
        date_index = stock_data[needed_data_length:, 1]
        result = pd.DataFrame(data=asset_daliy, index=date_index)
        self._summary[stock] = self._strategy.summary()
        self.asset_dict.update({stock: result})

    def summary(self):
        print self.asset_dict
        for x in self.asset_dict:
            self.asset_dict[x].plot()
            plt.show()
        print self._buy_record_list
        print self._sell_record_list
        return self._summary

    def get_stock_asset(self):
        pass
        # recordself.stock_asset.get_record(stock)


if __name__ == '__main__':
    import yaml
    import codecs

    with codecs.open('./test.yaml', encoding='utf-8') as f:
        data = yaml.load(f)
    print data
