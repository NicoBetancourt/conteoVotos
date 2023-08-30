import abc

class BaseController(abc.ABC):

    @abc.abstractmethod
    def create(self):
        ...

    @abc.abstractmethod
    def get(self):
        ...

    @abc.abstractmethod
    def update(self):
        ...

    @abc.abstractmethod
    def delete(self):
        ...
