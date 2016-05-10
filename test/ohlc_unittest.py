__author__ = 'squall'

import unittest
import pandas as pd
from data.ohlc import  OHLCVD


class MyTestCase(unittest.TestCase):
    def test_ohlc_add_all_feature(self):
        data = pd.read_csv('d:/stock/new-data/SH600741.TXT', sep='\t')
        print data.columns
        ohlc = OHLCVD(data.values)
        ohlc.add_all_ta_feature()
        data = ohlc.get_dataframe()
        print data.columns

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
