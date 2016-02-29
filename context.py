# coding=utf-8

"""
Context class is just a map.
"""

class Context(object):

    def __init__(self):
        self._object_dict = {}

    def get_object(self, key):
        """
        Get Object from the object map.
        :param key:
        :return:
        """
        if key in self._object_dict:
            return self._object_dict[key]
        else:
            return None