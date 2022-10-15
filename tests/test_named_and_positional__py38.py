from abc import abstractmethod, ABC
from typing import Literal

from overrides import override, EnforceOverrides


class A(EnforceOverrides):
    def methoda(self, x=0):
        print(x)

    def methodb(self, x: int, /, y: str) -> str:
        return y * x


class Other:
    def foo(self):
        pass


def test_should_pass():
    class B(A):
        @override
        def methoda(self, y=1, **kwargs):
            print(y)
            super().methoda(**kwargs)


def test_should_also_pass():
    class B(A):
        @override
        def methoda(self, z=1, x=1, **kwargs):
            pass


class Abs(ABC):
    @abstractmethod
    def method(self, str: Literal["max", "min"]):
        pass


def test_literal_passes():
    class B(Abs):
        @override
        def method(self, str: Literal["max", "min"]):
            return

    class C(Abs):
        @override
        def method(self, str: Literal["max", "min", "half"]):
            return


def test_literal_failure():
    try:

        class D(Abs):
            @override
            def method(self, str: Literal["a", "b", "c"]):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_literal_failure_not_accepting_all():
    try:

        class D(Abs):
            @override
            def method(self, str: Literal["min"]):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_can_not_override_with_positional_only():
    try:

        class C(A):
            @override
            def methoda(self, x=0, /):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_can_override_positional_only():
    class PositionalOnly1(A):
        @override
        def methodb(self, x: int, /, y: str) -> str:
            return "OK"


def test_can_override_positional_only_with_new_name():
    class PositionalOnly2(A):
        @override
        def methodb(self, new_name_is_ok: int, /, y: str) -> str:
            return "OK2"


def test_can_not_override_positional_only_with_new_type():
    try:

        class PositionalOnly3(A):
            @override
            def methodb(self, x: str, /, y: str) -> str:
                return "NOPE"

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_can_not_override_with_keyword_only():
    try:

        class C2(A):
            @override
            def methoda(self, *, x=0):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_multiple_inheritance():
    class Multi(A, Other):
        @override
        def methoda(self, y=2, **kwargs):
            pass

        @override
        def foo(self) -> int:
            pass
