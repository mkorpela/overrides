from abc import ABC, abstractmethod
from concurrent.futures import Future
from typing import Callable

from overrides import overrides


class MyInterface(ABC):
    @abstractmethod
    def run(self) -> "Future[str]":
        pass


class MyInterface2(ABC):
  @abstractmethod
  def run(self, callback: Callable[[str], None]):
    pass


def test_future_is_fine():
    class FutureWorks(MyInterface):
        @overrides
        def run(self) -> "Future[str]":
            pass


def test_callable_is_fine():
    class CallableWorks(MyInterface2):
        @overrides
        def run(self, callback: Callable[[str], None]):
            pass
