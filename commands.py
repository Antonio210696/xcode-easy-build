import abc


class ICommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def performAction(self):
        pass
