from abc import ABC, abstractmethod


class UnitOfWork(ABC):

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError()

    @abstractmethod
    def is_authenticated(self, *args, **kwargs) -> bool:
        raise NotImplementedError()
