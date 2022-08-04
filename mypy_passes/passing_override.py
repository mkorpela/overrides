from typing import Tuple

from overrides import overrides


class Parent:
    def execute(self, x: int, y: str, z: bool, *args, **kwargs) -> Tuple[str, int]:
        return y, x


class Child(Parent):
    @overrides
    def execute(self, *args, **kwargs) -> Tuple[str, int]:
        return "moi", 1
