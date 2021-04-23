from abc import ABCMeta
import inspect
from inspect import Parameter, Signature
from typing import Callable

import typing_utils


def ensure_compatible(
    x: Callable,
    y: Callable,
) -> None:
    """Ensure that the signature of `y` is compatible with the signature of `x`.

    Guarantees that any call to `x` will work on `y` by checking the following criteria:

    1. The return type of `y` is a subtype of the return type of `x`.
    2. All parameters of `x` are present in `y`, unless `y` declares `*args` or `**kwargs`.
    3. All positional parameters of `x` appear in the same order in `y`.
    4. All parameters of `x` are a subtype of the corresponding parameters of `y`.
    5. All required parameters of `y` are present in `x`, unless `x` declares `*args` or `**kwargs`.

    :param x: Function to check compatibility with.
    :param y: Function to check compatibility of.
    """
    x_sig = inspect.signature(x)
    y_sig = inspect.signature(y)

    # Verify that the return type of `y` is a subtype of `x`.
    if x_sig.return_annotation != Signature.empty \
        and y_sig.return_annotation != Signature.empty \
        and not typing_utils.issubtype(y_sig.return_annotation, x_sig.return_annotation):
        raise TypeError(f"`{y_sig.return_annotation}` is not a `{x_sig.return_annotation}`.")

    # Verify that all parameters in `x` are specified in `y` and that their types are compatible.
    y_var_args = any(p.kind == Parameter.VAR_POSITIONAL for p in y_sig.parameters.values())
    y_var_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in y_sig.parameters.values())

    for x_index, (name, x_param) in enumerate(x_sig.parameters.items()):
        if name not in y_sig.parameters \
            and not (x_param.kind == Parameter.VAR_POSITIONAL and not y_var_args) \
            and not (x_param.kind == Parameter.VAR_KEYWORD and not y_var_kwargs) \
            and not (x_param.kind == Parameter.POSITIONAL_ONLY and y_var_args) \
            and not (x_param.kind == Parameter.POSITIONAL_OR_KEYWORD and y_var_args and y_var_kwargs) \
            and not (x_param.kind == Parameter.KEYWORD_ONLY and y_var_kwargs):
            raise TypeError(f"`{name}` is not present.")
        elif name in y_sig.parameters \
            and not (x_param.kind == Parameter.VAR_POSITIONAL) \
            and not (x_param.kind == Parameter.VAR_KEYWORD):
            y_index = list(y_sig.parameters.keys()).index(name)
            y_param = y_sig.parameters[name]
            
            if x_param.kind != y_param.kind \
                and not (x_param.kind == Parameter.POSITIONAL_ONLY and y_param.kind == Parameter.POSITIONAL_OR_KEYWORD) \
                and not (x_param.kind == Parameter.KEYWORD_ONLY and y_param.kind == Parameter.POSITIONAL_OR_KEYWORD):
                raise TypeError(f"`{name}` is not `{x_param.kind.description}`")
            elif x_param.kind != Parameter.KEYWORD_ONLY and x_index != y_index:
                raise TypeError(f"`{name}` is not parameter `{x_index}`")
            elif x_param.annotation != Parameter.empty \
                and y_param.annotation != Parameter.empty \
                and not typing_utils.issubtype(x_param.annotation, y_param.annotation):
                raise TypeError(f"`{name} must be a supertype of `{x_param.annotation}`")

    # Verify that no parameters are specified in `y` that are not specified in `x`.
    x_var_args = any(p.kind == Parameter.VAR_POSITIONAL for p in x_sig.parameters.values())
    x_var_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in x_sig.parameters.values())
    
    for name, y_param in y_sig.parameters.items():
        if name not in x_sig.parameters \
            and y_param.default == Parameter.empty \
            and not (y_param.kind == Parameter.VAR_POSITIONAL) \
            and not (y_param.kind == Parameter.VAR_KEYWORD) \
            and not (y_param.kind == Parameter.KEYWORD_ONLY and x_var_kwargs) \
            and not (y_param.kind == Parameter.POSITIONAL_ONLY and x_var_args) \
            and not (y_param.kind == Parameter.POSITIONAL_OR_KEYWORD and x_var_args):
            raise TypeError(f"`{name}` is not a valid parameter.")


class EnforceOverridesMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
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
                if not base_class_method or not callable(base_class_method):
                    continue
                assert (
                    is_override
                ), "Method %s overrides but does not have @overrides decorator" % (name)
                # `__finalized__` is added by `@final` decorator
                assert not getattr(base_class_method, "__finalized__", False), (
                    "Method %s is finalized in %s, it cannot be overridden"
                    % (base_class_method, base)
                )
                ensure_compatible(base_class_method, value)
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
