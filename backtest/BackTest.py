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
        self._begin_date = config['begin']
        self._end_date = config['end']
        # Use database to store data.

        self._database = DBUtil(config['user'], str(config['passwd']), config['database'])
        self._summary = {}
        self._strategy = None
        self.stock_asset = RecordContainer()

    def set_strategy(self, strategy):
        self._strategy = strategy

    def test_strategy(self):
        if self._strategy is None:
            raise ValueError("Do not have a strategy")
        for stock in self._backtest_list:
            self._strategy.init(self._fund)
            stock_data = self._database.get_array(stock, self._begin_date, self._end_date)
            self._test_strategy(stock, stock_data)

    def buy_strategy(self, name, data):
        """
        Here is just a sample buy strategy.
        :param data:
        :return:
        """
        number = np.floor(self._fund/(data[4]*100))
        if number != 0:
            record = Record(name=name, date=data[1], number=number, price=data[4], tax=0, buy=True)
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
        sell_record = Record(name=name, price=data[4], number=record.number, tax=0, sell=True)
        self.stock_asset.add_record(sell_record)
        self._sell_record_list.append(sell_record)

    def _test_strategy(self, stock, stock_data):
        needed_data_length = self._strategy.get_data_need()
        for i in range(needed_data_length, stock_data.shape[0]):
            tmp_data = stock_data[(i-needed_data_length):i]
            if_buy = self._strategy.if_buy(tmp_data[-1])
            if if_buy:
                record = self.buy_strategy(stock, tmp_data[-1])
                continue
            if_sell = self._sell_strategy.if_sell(tmp_data[-1])
            if if_sell:
                record = self._strategy.sell(stock, tmp_data[-1])
                print record
                self._sell_record_list.append(record)
        self._summary[stock] = self._strategy.summary()

    def summary(self):
        return self._summary


def _load_stock_data(stock, begin, end):
    '''
    return: A pandas like data. Structure data.
    '''
    pass


if __name__ == '__main__':
    import yaml
    import codecs

    with codecs.open('./test.yaml', encoding='utf-8') as f:
        data = yaml.load(f)
    print data
