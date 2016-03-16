# coding=utf-8

import logging


def get_module_logger(mod_name):
    """
  create log for different moduler
  :param mod_name:
  :return:
  """

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    file_handler = logging.FileHandler(mod_name + ".log")
    file_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
