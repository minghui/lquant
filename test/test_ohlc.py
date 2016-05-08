__author__ = 'squall'

import unittest
from backtest.utils.mysql import MySQLUtils
from data.ohlc import OHLCVD


class MyTestCase(unittest.TestCase):
    def test_something(self):
        db = MySQLUtils('root', '1988', 'test', 'stock')
        data = db.get_array('sh600741', begin='2015-01-01', end='2016-01-01')
        ohlc = OHLCVD(data)
        ohlc.add_macd()
        ohlc.add_ma(10)
        ohlc.add_rsi_feature()
        ohlc.add_raise_day(5)
        ohlc.add_raise_day(10)
        ohlc.add_recent_down_v_turn()
        data = ohlc.get_array()

        print data.shape[1]
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
