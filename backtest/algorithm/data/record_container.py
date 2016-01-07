# coding=utf-8

import numpy as np
from record import Record


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
            print 'go here'
            self._stock_records[record.name] += record
        else:
            print 'go here 1'
            self._stock_records.update({record.name: record})

    def get_record(self, name):
        return self._stock_records[name]

    def get_stock_list(self):
        """
        :return: list
        """
        return self._stock_records.keys()

    def get_stock_money(self):
        """
        :return: float
        """
        tmp = [x.price*x.number for x in self._stock_records.values()]
        return np.sum(tmp)


if __name__ == '__main__':
    record_container = RecordContainer()
    record = Record(name='fuck', price=10.0, number=10, buy=True)
    record_container.add_record(record)
    record2 = Record(name='fuck', price=20.0, number=20, sell=True)
    record_container.add_record(record2)
    print record_container.get_stock_money()
    print record_container.get_stock_list()
    print record_container.get_record('fuck')