# coding=utf-8

from abc import abstractmethod


class Configurable(object):

    class ConfigureResult(object):

        def __init__(self):
            self.message = ""
            self.successed = True

    @abstractmethod
    def init_from_config(self, configure, **kwargs):
        pass

    @abstractmethod
    def get_from_context(self, context):
        pass

    @abstractmethod
    def set_to_context(self, context):
        pass



