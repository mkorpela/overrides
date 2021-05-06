from abc import ABC, abstractmethod
from concurrent.futures import Future
from typing import Callable


class MyInterface(ABC):
    @abstractmethod
    def run(self) -> "Future[str]":
        pass


class MyInterface2(ABC):
  @abstractmethod
  def run(self, callback: Callable[[str], None]):
    pass


def test_everything_here_is_fine():
    pass
