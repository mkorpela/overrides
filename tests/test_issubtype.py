from typing import Dict, Any, TypedDict

from overrides.typing_utils import issubtype


class MyTypedDict(TypedDict):
    foo: float
    bar: float


class Typed2(TypedDict):
    zoo: float


class Typed3(MyTypedDict, Typed2):
    pass


def test_typeddict_and_dict():
    assert issubtype(Typed3, Typed2)
    assert issubtype(Typed3, MyTypedDict)
    assert issubtype(MyTypedDict, Dict[str, Any])
