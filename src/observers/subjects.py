import subprocess
import threading
from abc import ABCMeta, abstractmethod
import shlex


class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    process_output = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer):
        # print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self):
        """
        Trigger an update in each subscriber.
        """

        # print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def start_process(self, commands):
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        def target():
            for command in commands:
                self.process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                while True:
                    output = self.process.stdout.readline().decode()
                    if output == '' and self.process.poll() is not None:
                        self.process_output = 'hamada'
                        self.notify()
                        break
                    if output:
                        self.process_output = output
                        self.notify()

        self.thread = threading.Thread(target=target)
        self.thread.setDaemon(True)
        self.thread.start()

    def __del__(self):
        if self.thread.is_alive():
            self.thread.join()
