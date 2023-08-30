import abc
from typing import Any, Optional


class RepositoryReader(abc.ABC):
    @abc.abstractmethod
    def get_one(self, id: int):
        ...

    @abc.abstractmethod
    def get_all(self, filter: Optional[Any]):
        ...

    @abc.abstractmethod
    def create(self):
        ...

    @abc.abstractmethod
    def update(self, id: int):
        ...

    @abc.abstractmethod
    def delete(self, id: int):
        ...
