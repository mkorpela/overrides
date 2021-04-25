import inspect
from inspect import Parameter
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
    if (hasattr(super_callable, "__self__") and hasattr(super_callable, "__func__")):
        super_callable = super_callable.__func__
    if (hasattr(sub_callable, "__self__") and hasattr(sub_callable, "__func__")):
        sub_callable = sub_callable.__func__
    super_sig = inspect.signature(super_callable)
    super_type_hints = get_type_hints(super_callable)
    sub_sig = inspect.signature(sub_callable)
    sub_type_hints = get_type_hints(sub_callable)

    ensure_return_type_compatibility(super_type_hints, sub_type_hints)
    ensure_all_args_defined_in_sub(super_sig, sub_sig, super_type_hints, sub_type_hints)
    ensure_no_extra_args_in_sub(super_sig, sub_sig)


def ensure_all_args_defined_in_sub(
    super_sig, sub_sig, super_type_hints, sub_type_hints
):
    sub_has_var_args = any(
        p.kind == Parameter.VAR_POSITIONAL for p in sub_sig.parameters.values()
    )
    sub_has_var_kwargs = any(
        p.kind == Parameter.VAR_KEYWORD for p in sub_sig.parameters.values()
    )
    for super_index, (name, super_param) in enumerate(super_sig.parameters.items()):
        if not is_param_defined_in_sub(
            name, sub_has_var_args, sub_has_var_kwargs, sub_sig, super_param
        ):
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
            elif (
                super_index != sub_index and super_param.kind != Parameter.KEYWORD_ONLY
            ):
                raise TypeError(f"`{name}` is not parameter `{super_index}`")
            elif (
                name in super_type_hints
                and name in sub_type_hints
                and not issubtype(super_type_hints[name], sub_type_hints[name])
            ):
                raise TypeError(
                    f"`{name} must be a supertype of `{super_param.annotation}`"
                )


def is_param_defined_in_sub(
    name, sub_has_var_args, sub_has_var_kwargs, sub_sig, super_param
):
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
            and not (
                sub_param.kind == Parameter.POSITIONAL_OR_KEYWORD and super_var_args
            )
        ):
            raise TypeError(f"`{name}` is not a valid parameter.")


def ensure_return_type_compatibility(super_type_hints, sub_type_hints):
    if (
        "return" in super_type_hints
        and "return" in sub_type_hints
        and not issubtype(sub_type_hints["return"], super_type_hints["return"])
    ):
        raise TypeError(
            f"`{sub_type_hints['return']}` is not a `{super_type_hints['return']}`."
        )
