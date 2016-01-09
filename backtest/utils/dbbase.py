# coding=utf-8

from abc import abstractmethod


class DBBase(object):

    def __init__(self):
        self._column_name = None

    @abstractmethod
    def current_state(self):
        pass

    @abstractmethod
    def current_time(self):
        pass

    def get_column_name(self):
        return self._column_name

    def set_column_name(self, column_name):
        self._column_name - column_name

    @abstractmethod
    def get_dataframe(self, id, begin=None, end=None, **kwargs):
        pass

    @abstractmethod
    def get_array(self, id, begin=None, end=None, **kwargs):
        pass