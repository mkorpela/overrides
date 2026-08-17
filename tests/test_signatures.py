from typing import Any, Callable, Type, Union

from overrides import override


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
    @override
    def foo(self, x: "ForwardReferencer") -> "ForwardReferencer":
        pass


class ClassMethodOverrider(SuperbClass):
    @classmethod
    @override
    def class_method(cls):
        pass


class StaticMethodOverrider(SuperbClass):
    @staticmethod
    @override
    def static_method(param: Union[str, bool]) -> int:
        return 3 if param == "bar" else 2


class NormalMethodOverrider(SuperbClass):
    @override
    def normal_method(self, x: int, y: str = "zoo", *args, **kwargs) -> bool:
        return x % 3 == 1 or y in kwargs or x == len(args)


class OverridesWithSignatureIgnore(SuperbClass):
    @override(check_signature=False)
    def normal_method(self, x: int) -> bool:
        return x % 2 == 1


class SelfTypedOverride(SuperbClass):
    @override(check_at_runtime=True)
    def self_typed_method(self: "SelfTypedOverride") -> "SelfTypedOverride":
        return self

    @classmethod
    @override(check_at_runtime=True)
    def self_typed_class_method(cls: "Type[SelfTypedOverride]") -> None:
        return None


class A:
    def foo(self: int):
        pass


class B(A):
    @override
    def foo(self: str):
        pass


class UntypedBaseClass:
    def do_something(self, arg1, arg2=None):
        pass


def test_typed_subclass_in_same_package_is_an_error():
    try:

        class TypedSubclass(UntypedBaseClass):
            @override
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


# --- Callable parameter contravariance (gh-113) -----------------------------
#
# A Callable's own *parameter types* are contravariant: a callback that
# accepts a narrower/more specific type is a valid substitute for one that
# accepts a wider type, so a subclass method is allowed to narrow the
# argument type of a Callable parameter relative to the superclass method.


class CallableArgX:
    pass


class CallableArgY(CallableArgX):
    pass


class CallableParamBase:
    def f(self, callback: Callable[[CallableArgX], None]) -> None:
        pass


class CallableParamNarrowed(CallableParamBase):
    # Callable[[Y], None] legitimately satisfies a contract requiring
    # Callable[[X], None], because Y is narrower than X and Callable
    # parameters are contravariant.
    @override
    def f(self, callback: Callable[[CallableArgY], None]) -> None:
        pass


class CallableParamBaseNarrow:
    def f(self, callback: Callable[[CallableArgY], None]) -> None:
        pass


class CallableReturnBase:
    def f(self, callback: Callable[[], CallableArgY]) -> None:
        pass


class CallableReturnWidened(CallableReturnBase):
    # Return types inside a Callable stay covariant. Since the Callable
    # itself is a (contravariant) parameter of f, the sub's Callable must be
    # a *supertype* of the super's Callable -- which, for return types,
    # means the sub's Callable may return a *base* class of what the
    # super's Callable returns.
    @override
    def f(self, callback: Callable[[], CallableArgX]) -> None:
        pass


class CallableReturnBaseNarrow:
    def f(self, callback: Callable[[], CallableArgX]) -> None:
        pass


def test_narrowing_callable_parameter_arg_type_is_allowed():
    CallableParamNarrowed().f(lambda y: None)


def test_widening_callable_parameter_arg_type_is_an_error():
    # The reverse is genuinely unsafe: overriding a Callable[[Y], None]
    # requirement with Callable[[X], None] would let the subclass call the
    # callback with an X that isn't necessarily a Y.
    try:

        class CallableParamWidened(CallableParamBaseNarrow):
            @override
            def f(self, callback: Callable[[CallableArgX], None]) -> None:
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


class CallableEllipsisParamBase:
    def f(self, callback: Callable[[CallableArgX], None]) -> None:
        pass


class CallableEllipsisParamOverride(CallableEllipsisParamBase):
    # Callable[..., X] means "unknown/any parameters" and must not be
    # treated as a plain parameter-type sequence -- it should be accepted
    # rather than raising when compared against an explicit parameter list.
    @override
    def f(self, callback: Callable[..., None]) -> None:
        pass


class CallableEllipsisParamBaseReverse:
    def f(self, callback: Callable[..., None]) -> None:
        pass


class CallableEllipsisParamOverrideReverse(CallableEllipsisParamBaseReverse):
    @override
    def f(self, callback: Callable[[CallableArgX], None]) -> None:
        pass


def test_callable_ellipsis_parameter_list_does_not_raise():
    CallableEllipsisParamOverride().f(lambda x: None)
    CallableEllipsisParamOverrideReverse().f(lambda x: None)


def test_callable_return_type_covariance_is_unaffected():
    CallableReturnWidened().f(lambda: CallableArgX())

    # The reverse (narrowing the return type) is not a valid supertype and
    # must still be rejected.
    try:

        class CallableReturnNarrowed(CallableReturnBaseNarrow):
            @override
            def f(self, callback: Callable[[], CallableArgY]) -> None:
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass
