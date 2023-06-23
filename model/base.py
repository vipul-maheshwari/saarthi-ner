import logging
from abc import ABC

class ModelBase(ABC):
    def __init__(self, max_seq_len, strategy, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.max_seq_len = max_seq_len
        self.strategy = strategy
