# coding=utf-8

from data.record import Record
from backtest.utils.tax import *


class RecordContainer(object):
    """
    This class is used to contain the record.
    When add record to the container, container should compute the
    """
    def __init__(self):
        self._stock_records = {}
        self._stock_money = None

    def add_record(self, record):
        if self._stock_records.__contains__(record.name):
            if record.buy == True:
                self._stock_records[record.name] += record
            else:
                self._stock_records[record.name] -= record
        else:
            self._stock_records.update({record.name: record})
        self._sync()

    def get_record(self, name):
        if name in self._stock_records:
            return self._stock_records[name]
        return None

    def get_stock_list(self):
        """
        :return: list
        """
        return self._stock_records.keys()

    def get_stock_cost_money(self):
        """
        :return: float
        """
        tmp = [x.price*x.number for x in self._stock_records.values()]
        return np.sum(tmp)

    def _sync(self):
        """
        Update the stock asset, stock number is zero will be delete
        :return:
        """
        # for x in self._stock_records:
        #     if self._stock_records[x].number == 0:
        #         del self._stock_records[x]
        pass

    def clear(self):
        self._stock_records = {}


if __name__ == '__main__':
    record_container = RecordContainer()
    record = Record(name='fuck', price=10.0, number=10, buy=True)
    record_container.add_record(record)
    record2 = Record(name='fuck', price=20.0, number=10, sell=True)
    record_container.add_record(record2)
    print record_container.get_record('fuck')
    print record_container.get_stock_cost_money()
    print record_container.get_stock_list()
    print record_container.get_record('fuck')