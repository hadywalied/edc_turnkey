import logging

from src.logging.logers import Loggers

try:
    from cStringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO


class LevelFilter(logging.Filter):
    def __init__(self, levels):
        self.levels = levels

    def filter(self, record):
        return record.levelno in self.levels


if __name__ == "__main__":
    loggers = Loggers(".")
    loggers.sendState("this is a message")
    loggers.sendState("error: this is an error")
    loggers.sendState("warning: this is a warining")
