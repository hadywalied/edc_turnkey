import logging
import sys


class Loggers:
    def __init__(self, logPath = ".", info_fileName="info", error_fileName="error"):
        self.state = ""
        self.infoLogger = logging.getLogger("info")
        logFormatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, info_fileName))
        fileHandler.setFormatter(logFormatter)
        self.infoLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        self.infoLogger.addHandler(consoleHandler)
        self.infoLogger.setLevel(logging.DEBUG)

        self.fatalLogger = logging.getLogger("error")
        logFormatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, error_fileName))
        fileHandler.setFormatter(logFormatter)
        self.fatalLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        self.fatalLogger.addHandler(consoleHandler)
        self.fatalLogger.setLevel(logging.DEBUG)

    def sendState(self, state):
        self.state = state
        if state.__contains__('error'):
            self.log_error()
        elif state.__contains__("warning"):
            self.log_warning()
        else:
            self.log_info()

    def log_info(self):
        self.infoLogger.info(msg=self.state)

    def log_warning(self):
        self.fatalLogger.warning(msg=self.state)

    def log_error(self):
        self.fatalLogger.error(msg=self.state)
