# coding=utf-8


class Order(object):
    """
    Order class is used to save the buy or sell order, but now I have a problem
    if I should add the current price to the order structure. If added. I should
    add current_date too. At the same time, tax is a problem, it is a little
    tick to calculate the tax.
    """

    def __init__(self, name=None, price=None, number=None, tax=0, date=None,
                 current_price=None,
                 buy=False, sell=False, **kwargs):
        """
        This is the record class which is used to save the record of every buy
        or sell event.
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
        # Here price is the buy or sell price. Current price is saved in current_price variable.
        self.price = price
        self.tax = tax
        self.buy_date = date
        self.buy = buy
        self.sell = sell
        self.number = number
        self.return_rate = 0.0
        self.current_price = current_price
        self.__dict__.update(kwargs)

    def __add__(self, new_order):
        if not isinstance(new_order, Order):
            raise ValueError('Must a Record class')
        if self.name == new_order.name:
            # FIXME: This is bullshit.
            if new_order.sell:
                return self - new_order
            price = (self.number*self.price +
                     new_order.number*new_order.price)/(self.number+new_order.number)
            number = self.number + new_order.number
            # FIXME: Should not return self, but a new record.
            # Here should change.
            return Order(name=self.name, price=price, tax=self.tax,
                         number=number, date=self.buy_date, buy=self.buy,
                         current_price=new_order.current_price,
                         sell=self.buy)
        else:
            raise ValueError('Only same stock can add.')

    def __sub__(self, new_order):
        """
        Sub method, maybe it is useless.
        :type new_order: Order
        """
        if not isinstance(new_order, Order):
            raise ValueError('Must a Record class can sub')
        if self.name == new_order.name:
            if self.number < new_order.number:
                raise ValueError('Can not sell more stock than have.')
            return_value = (new_order.number*new_order.price) - \
                           (new_order.number*self.price)
            # self.number -= record.number
            number = self.number - new_order.number
            # if self.number != 0:
            #     # self.price = (self.price*self.number
            #     # - return_value)/self.number
            #     price = (self.price*self.number - return_value)/self.number
            # else:
            #     # self.price = -return_value/record.number
            #     price = -return_value/new_order.number
            # Do not change the price we buy the stock.
            return Order(name=self.name, price=self.price, number=number,
                         tax=self.tax, date=self.buy_date, buy=self.buy,
                         sell=self.sell)
        else:
            raise ValueError('Only same stock can sub.')

    def __repr__(self):
        return 'None'
        # buy_print_str = '''This is the buy record of %s , cost price is: %s,
        # number is: %s, date is: %s'''
        # sell_print_str = '''This is the sell record of %s , cost price is: %s,
        # number is: %s, date is: %s'''
        # if self.buy:
        #     return buy_print_str % (self.name, self.price, self.number,
        #                             self.buy_date)
        # elif self.sell:
        #     return sell_print_str % (self.name, self.price, self.number,
        #                              self.buy_date)
        # else:
        #     return 'Do not have record'

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
    record1 = Order(name='test', number=100.0, price=15.0, tax=5, sell=True)
    result = order-record1
    result2 = order + record1
    print "This is the result 2:", result2
    print result
    print order
    result = order + record1
    print result

