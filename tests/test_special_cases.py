from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from concurrent.futures import Future
from typing import Callable, Any

import pytest

from overrides import EnforceOverrides, override


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
        @override
        def run(self) -> "Future[str]":
            pass


def test_callable_is_fine():
    class CallableWorks(MyInterface2):
        @override
        def run(self, callback: Callable[[str], None]):
            pass


def test_overriding_untyped_from_other_package_is_fine():
    class Params(MutableMapping):
        DEFAULT = object()

        @override
        def pop(
            self, key: str, default: Any = DEFAULT, keep_as_dict: bool = False
        ) -> Any:
            pass


def test_overriding_method_of_sibling_nested_class_is_fine():
    # Regression test for https://github.com/mkorpela/overrides/issues/86
    # `Bar` is only reachable as a local variable in the enclosing `Foo`
    # class body, not as a module global, so resolving it requires
    # consulting the calling frame's locals.
    class Foo:
        class Bar(EnforceOverrides):
            def to_dict(self):
                return {}

        class Car(Bar):
            @override
            def to_dict(self):
                return {"car": True}

    assert Foo.Car().to_dict() == {"car": True}


def test_overriding_method_of_sibling_nested_class_still_validates():
    # The base class resolved for the nested-class case must be the
    # actual `Bar` class, not something incidentally found elsewhere, so
    # a genuinely incompatible override still raises.
    with pytest.raises(TypeError):

        class Foo:
            class Bar(EnforceOverrides):
                def to_dict(self):
                    return {}

            class Car(Bar):
                @override
                def not_a_base_method(self):
                    pass
