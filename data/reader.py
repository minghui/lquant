# coding=utf-8


class Reader(object):

    def __init__(self):
        self.data = None
        self.data_frame = None

    def get_data(self):
        return self.data

    def get_dataframe(self):
        return self.data_frame


class OHLCReader(Reader):

    def __init__(self):
        super(Reader, self).__init__()
        self._header = ["date", "open", "high", "low", "close", "volume",
                        "deal"]

    def add_feature(self, *args, **kwargs):
        raise NotImplementedError
