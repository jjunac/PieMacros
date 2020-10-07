import logging

def init_logging():
    logging.basicConfig(format='%(asctime)s %(name)-20.20s %(levelname)-6s %(message)s', level=logging.DEBUG)

def logger(cls):
    cls._logger = logging.getLogger(cls.__name__)
    return cls