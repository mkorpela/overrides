from overrides import overrides, EnforceOverrides


class A(EnforceOverrides):
    def methoda(self, x=0):
        print(x)


def test_should_pass():
    class B(A):
        @overrides
        def methoda(self, y=1, **kwargs):
            print(y)
            super().methoda(**kwargs)
