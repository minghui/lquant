__author__ = 'squall'

import unittest
import pandas as pd
from data.ohlc import OHLCVD
from backtest.utils.mysql import MySQLUtils
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_ohlc_add_all_feature(self):
        data = pd.read_csv('d:/stock/new-data/SH600741.TXT', sep='\t')
        ohlc = OHLCVD(data.values)
        ohlc.add_all_ta_feature()
        data = ohlc.get_dataframe()
        result = data.replace(np.nan, -1.0).replace(np.inf, -2.0).replace(-np.inf, -3.0)


        sql_line = '''insert into stock_with_feature values('sh600741', '%s', %s )'''%(result.values[1, 0],
                                                                                       ','.join([str(x) for x in result.values[1, 1:]]), )

        print sql_line
        db = MySQLUtils('root', '1988', 'stock', 'stock_with_feature')

        db.execute_sql(sql_line)
        self.assertEqual(ohlc.data.shape[1], 149)


if __name__ == '__main__':
    unittest.main()
