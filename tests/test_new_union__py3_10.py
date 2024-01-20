from __future__ import annotations

import sys

import pytest
from overrides import override


class A:
    def f(self) -> int | str:
        return 1


def test_should_allow_reducing_type():
    class B(A):
        @override
        def f(self) -> int:
            return 1

    assert B().f() == 1


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python3.10 or higher")
def test_should_not_allow_increasing_type():
    with pytest.raises(TypeError):

        class C(A):
            @override
            def f(self) -> int | str | list[str]:
                return []

        assert False, "should not go here"
