import inspect
from abc import ABCMeta
from inspect import Parameter, Signature
from types import FunctionType
from typing import Callable, TypeVar, Union, get_type_hints

from typing_utils import issubtype  # type: ignore

_WrappedMethod = TypeVar("_WrappedMethod", bound=Union[FunctionType, Callable])

def ensure_signature_is_compatible(
    super_callable: _WrappedMethod,
    sub_callable: _WrappedMethod,
) -> None:
    """Ensure that the signature of `sub_callable` is compatible with the signature of `super_callable`.

    Guarantees that any call to `super_callable` will work on `sub_callable` by checking the following criteria:

    1. The return type of `sub_callable` is a subtype of the return type of `super_callable`.
    2. All parameters of `super_callable` are present in `sub_callable`, unless `sub_callable`
       declares `*args` or `**kwargs`.
    3. All positional parameters of `super_callable` appear in the same order in `sub_callable`.
    4. All parameters of `super_callable` are a subtype of the corresponding parameters of `sub_callable`.
    5. All required parameters of `sub_callable` are present in `super_callable`, unless `super_callable`
       declares `*args` or `**kwargs`.

    :param super_callable: Function to check compatibility with.
    :param sub_callable: Function to check compatibility of.
    """
    super_sig = inspect.signature(super_callable)
    super_type_hints = get_type_hints(super_callable)
    sub_sig = inspect.signature(sub_callable)
    sub_type_hints = get_type_hints(sub_callable)

    ensure_return_type_compatibility(super_type_hints, sub_type_hints)
    ensure_all_args_defined_in_sub(super_sig, sub_sig, super_type_hints, sub_type_hints)
    ensure_no_extra_args_in_sub(super_sig, sub_sig)


def ensure_all_args_defined_in_sub(super_sig, sub_sig, super_type_hints, sub_type_hints):
    sub_has_var_args = any(
        p.kind == Parameter.VAR_POSITIONAL for p in sub_sig.parameters.values()
    )
    sub_has_var_kwargs = any(
        p.kind == Parameter.VAR_KEYWORD for p in sub_sig.parameters.values()
    )
    for super_index, (name, super_param) in enumerate(super_sig.parameters.items()):
        if not is_param_defined_in_sub(name, sub_has_var_args, sub_has_var_kwargs, sub_sig, super_param):
            raise TypeError(f"`{name}` is not present.")
        elif (
                name in sub_sig.parameters
                and super_param.kind != Parameter.VAR_POSITIONAL
                and super_param.kind != Parameter.VAR_KEYWORD
        ):
            sub_index = list(sub_sig.parameters.keys()).index(name)
            sub_param = sub_sig.parameters[name]

            if (
                    super_param.kind != sub_param.kind
                    and not (
                    super_param.kind == Parameter.POSITIONAL_ONLY
                    and sub_param.kind == Parameter.POSITIONAL_OR_KEYWORD
            )
                    and not (
                    super_param.kind == Parameter.KEYWORD_ONLY
                    and sub_param.kind == Parameter.POSITIONAL_OR_KEYWORD
            )
            ):
                raise TypeError(f"`{name}` is not `{super_param.kind.description}`")
            elif super_index != sub_index and super_param.kind != Parameter.KEYWORD_ONLY:
                raise TypeError(f"`{name}` is not parameter `{super_index}`")
            elif (
                    name in super_type_hints
                    and name in sub_type_hints
                    and not issubtype(super_type_hints[name], sub_type_hints[name])
            ):
                raise TypeError(
                    f"`{name} must be a supertype of `{super_param.annotation}`"
                )


def is_param_defined_in_sub(name, sub_has_var_args, sub_has_var_kwargs, sub_sig, super_param):
    return (
            name in sub_sig.parameters
            or (super_param.kind == Parameter.VAR_POSITIONAL and sub_has_var_args)
            or (super_param.kind == Parameter.VAR_KEYWORD and sub_has_var_kwargs)
            or (super_param.kind == Parameter.POSITIONAL_ONLY and sub_has_var_args)
            or (
            super_param.kind == Parameter.POSITIONAL_OR_KEYWORD
            and sub_has_var_args
            and sub_has_var_kwargs
            )
            or (super_param.kind == Parameter.KEYWORD_ONLY and sub_has_var_kwargs)
    )


def ensure_no_extra_args_in_sub(super_sig, sub_sig):
    super_var_args = any(
        p.kind == Parameter.VAR_POSITIONAL for p in super_sig.parameters.values()
    )
    super_var_kwargs = any(
        p.kind == Parameter.VAR_KEYWORD for p in super_sig.parameters.values()
    )
    for name, sub_param in sub_sig.parameters.items():
        if (
                name not in super_sig.parameters
                and sub_param.default == Parameter.empty
                and sub_param.kind != Parameter.VAR_POSITIONAL
                and sub_param.kind != Parameter.VAR_KEYWORD
                and not (sub_param.kind == Parameter.KEYWORD_ONLY and super_var_kwargs)
                and not (sub_param.kind == Parameter.POSITIONAL_ONLY and super_var_args)
                and not (sub_param.kind == Parameter.POSITIONAL_OR_KEYWORD and super_var_args)
        ):
            raise TypeError(f"`{name}` is not a valid parameter.")


def ensure_return_type_compatibility(super_type_hints, sub_type_hints):
    if (
            'return' in super_type_hints
            and 'return' in sub_type_hints
            and not issubtype(sub_type_hints['return'], super_type_hints['return'])
    ):
        raise TypeError(
            f"`{sub_type_hints['return']}` is not a `{super_type_hints['return']}`."
        )


class EnforceOverridesMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        # Ignore any methods defined on the metaclass when enforcing overrides.
        for method in dir(mcls):
            if not method.startswith("__") and method != "mro":
                value = getattr(mcls, method)
                if not isinstance(value, (bool, str, int, float, tuple, list, dict)):
                    setattr(getattr(mcls, method), "__ignored__", True)

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        for name, value in namespace.items():
            # Actually checking the direct parent should be enough,
            # otherwise the error would have emerged during the parent class checking
            if name.startswith("__"):
                continue
            value = mcls.handle_special_value(value)
            is_override = getattr(value, "__override__", False)
            for base in bases:
                base_class_method = getattr(base, name, False)
                if not base_class_method or not callable(base_class_method) or getattr(base_class_method, "__ignored__", False):
                    continue
                assert (
                    is_override
                ), "Method %s overrides but does not have @overrides decorator" % (name)
                # `__finalized__` is added by `@final` decorator
                assert not getattr(
                    base_class_method, "__finalized__", False
                ), "Method %s is finalized in %s, it cannot be overridden" % (
                    base_class_method,
                    base,
                )
                ensure_signature_is_compatible(base_class_method, value)
        return cls

    @staticmethod
    def handle_special_value(value):
        if isinstance(value, classmethod) or isinstance(value, staticmethod):
            value = value.__get__(None, dict)
        elif isinstance(value, property):
            value = value.fget
        return value


class EnforceOverrides(metaclass=EnforceOverridesMeta):
    "Use this as the parent class for your custom classes"
    pass
