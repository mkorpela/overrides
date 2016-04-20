import sys

if sys.version < '3':
    from overrides import overrides
    from overrides import __VERSION__
else:
    from overrides.overrides import overrides
    from overrides.overrides import __VERSION__
