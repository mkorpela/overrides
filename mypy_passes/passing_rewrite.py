""""Bug."""
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

try:
    from overrides import override
except ModuleNotFoundError:

    def override(func: Callable[P, T]) -> Callable[P, T]:  # type: ignore[no-redef]
        return func


print(override)
