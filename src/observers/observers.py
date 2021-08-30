import sys
from abc import ABCMeta, abstractmethod

from src.observers.subjects import Subject


class Observer:
    """
    The Observer interface declares the update method, used by subjects.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, subject):
        """
        Receive update from subject.
        """
        pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


class ConcreteObserver(Observer):
    def __init__(self, logger, monitor):
        self.logger = logger
        self.moitor = monitor

    def update(self, subject):
        self.subject = subject
        # if subject.state.__contains__('error') or subject.state.__contains__('not found') \
        #         or subject.state.__contains__("down"):
        #     print('something went wrong: {output}'.format(output=subject.state))
        #     sys.exit(0)
        # print(subject.state)
        self.monitor.sendState(subject.process_output)
        self.logger.sendState(subject.process_output)

    def __del__(self):
        if self.subject.thread.is_alive():
            self.subject.process.terminate()
            self.subject.thread.join()
