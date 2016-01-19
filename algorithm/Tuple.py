# coding=utf-8

import numpy as np

from algorithm.Algorithm import AlgorithmBase


class Tuple(AlgorithmBase):

    def __init__(self):
        pass

    def set_paramter(self, *args, **kwargs):
        if 'n' not in kwargs.keys():
            raise ValueError('must contain parameter n')
        self._n_tuple = kwargs['n']

    def fit(self, X, Y):
        if not isinstance(X, list) and not isinstance(X, np.array):
            return None

        if len(X) < 100:
            return 'too few sample'

        for i in range(0, len(X)-self._n_tuple):
            pass


