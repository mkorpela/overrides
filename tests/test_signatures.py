from typing import Any, Type, Union

from overrides import overrides


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

    def self_typed_method(self: "SuperbClass") -> "SuperbClass":
        return self

    @classmethod
    def self_typed_class_method(cls: "Type[SuperbClass]") -> None:
        return None

    def foo(self, x) -> None:
        return None


class ForwardReferencer(SuperbClass):
    @overrides
    def foo(self, x: "ForwardReferencer") -> "ForwardReferencer":
        pass


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
    @overrides(check_signature=False)
    def normal_method(self, x: int) -> bool:
        return x % 2 == 1


class SelfTypedOverride(SuperbClass):
    @overrides(check_at_runtime=True)
    def self_typed_method(self: "SelfTypedOverride") -> "SelfTypedOverride":
        return self

    @classmethod
    @overrides(check_at_runtime=True)
    def self_typed_class_method(cls: "Type[SelfTypedOverride]") -> None:
        return None


class A:
    def foo(self: int):
        pass


class B(A):
    @overrides
    def foo(self: str):
        pass


class UntypedBaseClass:
    def do_something(self, arg1, arg2=None):
        pass


def test_typed_subclass_in_same_package_is_an_error():
    try:

        class TypedSubclass(UntypedBaseClass):
            @overrides
            def do_something(self, arg1: str, arg2: Any = None) -> Any:
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_that_this_file_is_ok():
    pass


def test_self_typed_overrides():
    SelfTypedOverride().self_typed_method()
    SelfTypedOverride().self_typed_class_method()
