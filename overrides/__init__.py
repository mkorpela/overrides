import sys

if sys.version < '3':
    from overrides import overrides
    from final import final
    from overrides import __VERSION__
    from enforce27 import EnforceOverrides
else:
    from overrides.overrides import overrides
    from overrides.final import final
    from overrides.overrides import __VERSION__
    from overrides.enforce import EnforceOverrides
