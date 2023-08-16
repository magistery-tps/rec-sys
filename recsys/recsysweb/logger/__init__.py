import logging


def get_logger(object): return logging.getLogger(object.__class__.__name__)