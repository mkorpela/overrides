from overrides import overrides, EnforceOverrides


class A(EnforceOverrides):
    def methoda(self, x=0):
        print(x)


class Other:
    def foo(self):
        pass


def test_should_pass():
    class B(A):
        @overrides
        def methoda(self, y=1, **kwargs):
            print(y)
            super().methoda(**kwargs)


def test_should_also_pass():
    class B(A):
        @overrides
        def methoda(self, z=1, x=1, **kwargs):
            pass


def test_can_not_override_with_positional_only():
    try:

        class C(A):
            @overrides
            def methoda(self, x=0, /):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_can_not_override_with_keyword_only():
    try:

        class C2(A):
            @overrides
            def methoda(self, *, x=0):
                pass

        raise AssertionError("Should not go here")
    except TypeError:
        pass


def test_multiple_inheritance():
    class Multi(A, Other):
        @overrides
        def methoda(self, y=2, **kwargs):
            pass

        @overrides
        def foo(self) -> int:
            pass
