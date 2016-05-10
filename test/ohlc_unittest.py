__author__ = 'squall'

import unittest
import pandas as pd
from data.ohlc import  OHLCVD


class MyTestCase(unittest.TestCase):

    def test_ohlc_add_all_feature(self):
        data = pd.read_csv('d:/stock/new-data/SH600741.TXT', sep='\t')
        ohlc = OHLCVD(data.values)
        ohlc.add_all_ta_feature()
        data = ohlc.get_dataframe()
        self.assertEqual(ohlc.data.shape[1], 149)


if __name__ == '__main__':
    unittest.main()
