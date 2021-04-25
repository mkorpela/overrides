from typing import Union

from overrides import overrides, overrides_ignore_signature


class SuperbClass:
    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method(param: str) -> int:
        if param == "foo":
            return 2
        return 1

    def normal_method(self, x: int, y: str = "hello", *args, **kwargs) -> bool:
        return x == 1 or y == "bar" or len(args) == 3 or "zoo" in kwargs


class ClassMethodOverrider(SuperbClass):
    @classmethod
    @overrides
    def class_method(cls):
        pass


class StaticMethodOverrider(SuperbClass):
    @staticmethod
    @overrides
    def static_method(param: Union[str, bool]) -> int:
        return 3 if param == "bar" else 2


class NormalMethodOverrider(SuperbClass):
    @overrides
    def normal_method(self, x: int, y: str = "zoo", *args, **kwargs) -> bool:
        return x % 3 == 1 or y in kwargs or x == len(args)


class OverridesWithSignatureIgnore(SuperbClass):
    @overrides_ignore_signature
    def normal_method(self, x: int) -> bool:
        return x % 2 == 1


def test_that_this_file_is_ok():
    pass
