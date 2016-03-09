# coding=utf-8


class Order(object):

    def __init__(self, name=None, price=None, number=None, tax=0, date=None,
                 buy=False, sell=False, **kwargs):
        """
        This is the record class which is used to save the record of every buy or sell event.
        :param name:
        :param price: This is the cost price.
        :param number: stock number
        :param tax:
        :param date:
        :param buy:
        :param sell:
        :param kwargs:
        :return:
        """
        self.name = name
        self.buy_price = price
        self.tax = tax
        self.date = date
        self.buy = buy
        self.sell = sell
        self.number = number
        self.return_rate = 0.0
        if "current_price" in kwargs:
            self.current_price = kwargs["current_price"]
        else:
            self.current_price = None
        self.__dict__.update(kwargs)

    def __add__(self, order):
        if not isinstance(order, Order):
            raise ValueError('Must a Record class')
        if self.name == order.name:
            # FIXME: This is bullshit.
            price = (self.number*self.buy_price+self.tax+order.tax+
                     order.number*order.buy_price)/(self.number+order.number)
            number = self.number + order.number
            # FIXME: Should not return self, but a new record. Here should change.
            return Order(name=self.name, price=price, tax=self.tax,
                         number=number, date=self.date, buy=self.buy,
                         sell=self.buy)
        else:
            raise ValueError('Only same stock can add.')

    def __sub__(self, order):
        """
        Sub method, maybe it is useless.
        :type order: Order
        """
        if not isinstance(order, Order):
            raise ValueError('Must a Record class can sub')
        if self.name == order.name:
            if self.number < order.number:
                raise ValueError('Can not sell more stock than have.')
            return_value = (order.number*order.buy_price-order.tax) - \
                           (order.number*self.buy_price)
            # self.number -= record.number
            number = self.number - order.number
            if self.number != 0:
                # self.price = (self.price*self.number - return_value)/self.number
                price = (self.buy_price*self.number - return_value)/self.number
            else:
                # self.price = -return_value/record.number
                price = -return_value/order.number
            return Order(name=self.name, price=price, number=number,
                          tax=self.tax, date=self.date, buy=self.buy,
                          sell=self.buy)
        else:
            raise ValueError('Only same stock can sub.')

    def __repr__(self):
        buy_print_str = '''This is the buy record of %s , cost price is: %s,
        number is: %s, date is: %s'''
        sell_print_str = '''This is the sell record of %s , cost price is: %s,
        number is: %s, date is: %s'''
        if self.buy:
            return buy_print_str % (self.name, self.buy_price, self.number,
                                    self.date)
        elif self.sell:
            return sell_print_str % (self.name, self.buy_price, self.number,
                                     self.date)
        else:
            return 'Do not have record'

    def set_tax(self, tax):
        self.tax = tax

    def get_dict(self):
        return self.__dict__

    @staticmethod
    def create_order(name, date, price, number):
        return Order(name=name, date=date, price=price, number=number)


if __name__ == '__main__':
    order = Order(name='test', number=200.0, price=10.0, tax=5, buy=True)
    print order
    record1 = Order(name='test', number=100.0, price=15.0, tax=5, buy=True)
    result = order-record1
    print result
    print order
    result = order + record1
    print result

