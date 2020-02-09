import sys
from typing import Callable, Any

overrides = lambda *args:0 # type: Callable[[Any], Any]

if sys.version < '3':
    from overrides import overrides # type: ignore
    from final import final # type: ignore
    from overrides import __VERSION__  # type: ignore
else:
    from overrides.overrides import overrides
    from overrides.final import final
    from overrides.overrides import __VERSION__
    from overrides.enforce import EnforceOverrides
