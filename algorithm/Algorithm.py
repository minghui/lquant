# coding=utf-8

'''
This is the base class of all the algorithm used in my project.
'''

from abc import abstractmethod


class AlgorithmBase(object):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_probs(self, X):
        '''
        Use the model to estimate the X.
        :param X: An numpy array, may be in some algorithm on will use window data.
        :return:
        '''
        pass

    @abstractmethod
    def fit(self, X, Y):
        '''
        Use data to fit a model, just like sklearn do.
        :param X: Array like data.
        :param Y: Array like data.
        :return:
        '''
        pass

    @abstractmethod
    def set_paramter(self, *args, **kwargs):
        '''
        Some Algorithm may need parameter to determine the model.
        :param args:
        :param kwargs:
        :return:
        '''
        pass

    @abstractmethod
    def pre_process(self, data=None, *args, **kwargs):
        '''
        This abstract method is used to pre-processing the data.
        :param data: User can define special data structure, but one must parse it self.
        :param args: Include all the args want used in the function.
        :param kwargs: Include all the dict args want used in the functioin.
        :return: If wrong return None or raise a ValueError.
        '''
        pass

    @abstractmethod
    def post_precess(self, data=None, *args, **kwargs):
        '''
        This abstract method is used to post process the data.
        :param data:
        :param args:
        :param kwargs:
        :return: If wrong return None or raise a ValueError.
        '''
        pass

    @abstractmethod
    def set_period(self, being, end):
        '''
        Use data period, if not define, begin is the most early date,
        end is the most latest date.
        :param being: Begin time of the data.
        :param end: End time of the data.
        :return:
        '''
        pass

