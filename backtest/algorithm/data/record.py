# coding=utf-8


class Record(object):

    def __init__(self, name=None, price=None, number=None, tax=0, date=None, buy=False, sell=False, **kwargs):
        self.name = name
        self.price = price
        self.tax = tax
        self.date = date
        self.buy = buy
        self.sell = sell
        self.number = number
        self.__dict__.update(kwargs)

    def __add__(self, record):
        if not isinstance(record, Record):
            raise ValueError('Must a Record class')
        if self.name == record.name:
            # FIXME: This is bullshit.
            # self.price = (self.number*self.price+self.tax+record.tax+record.number*record.price)/(self.number+record.number)
            # self.number += record.number
            price = (self.number*self.price+self.tax+record.tax+record.number*record.price)/(self.number+record.number)
            number = self.number + record.number
            print 'This is the price:', price
            print 'This is the number: ', number
            # FIXME: Should not return self, but a new record. Here should change.
            return Record(name=self.name, price=price, tax=self.tax, number=number, date=self.date, buy=self.buy,
                          sell=self.buy)
        else:
            raise ValueError('Only same stock can add.')

    def __sub__(self, record):
        if not isinstance(record, Record):
            raise ValueError('Must a Record class can sub')
        if self.name == record.name:
            if self.number < record.number:
                raise ValueError('Can not sell more stock than have.')
            return_value = (record.number*record.price-record.tax)-(record.number*self.price)
            # self.number -= record.number
            number = self.number - record.number
            if self.number != 0:
                # self.price = (self.price*self.number - return_value)/self.number
                price = (self.price*self.number - return_value)/self.number
            else:
                # self.price = -return_value/record.number
                price = -return_value/record.number
            return Record(name=self.name, price=price, number=number, tax=self.tax, date=self.date, buy=self.buy,
                          sell=self.buy)
        else:
            raise ValueError('Only same stock can sub.')

    def __repr__(self):
        if self.buy:
            return 'This is the buy record, price is: %s, number is: %s' % (self.price, self.number)
        elif self.sell:
            return 'This is the sell record, price is: %s, number is: %s' % (self.price, self.number)
        else:
            return 'Do not have record'



if __name__ == '__main__':
    record = Record(name='test', number=200.0, price=10.0, tax=5, buy=True)
    print record
    record1 = Record(name='test', number=100.0, price=15.0, tax=5, buy=True)
    result = record-record1
    print result
    print record
    result = record + record1
    print result

