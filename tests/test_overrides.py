import sys
import unittest
from contextlib import contextmanager
from typing import Generic, TypeVar

import test_somepackage
from overrides import overrides

TObject = TypeVar("TObject", bound="Foo")


@contextmanager
def no_error():
    yield


class SubClassOfGeneric(Generic[TObject]):
    def some_method(self):
        """Generic sub class."""
        pass


class SubSubClassOfGeneric(SubClassOfGeneric["SubSubClassOfGeneric"]):
    @overrides
    def some_method(self):
        return 17


class SuperClass(object):
    @staticmethod
    def this_is_static(x, y, z):
        pass

    def some_method(self):
        """Super Class Docs"""
        return "super"

    class SomeClass:
        """Super Inner Class Docs"""

        def check(self):
            return 0


class SubClass(SuperClass):
    @overrides
    def some_method(self):
        return "sub"


class Subber(SuperClass):
    @overrides
    def some_method(self):
        """Subber"""
        return 1


class Sub2(test_somepackage.SomeClass, SuperClass):
    @overrides
    def somewhat_fun_method(self):
        return "foo"

    @overrides
    def some_method(self):
        pass


class SubclassOfInt(int):
    @overrides
    def __str__(self):
        return "subclass of int"


class CheckAtRuntime(SuperClass):
    @overrides(check_at_runtime=True)
    def some_method(self, x):
        pass


class StaticMethodOverridePass(SuperClass):
    @staticmethod
    @overrides
    def this_is_static(x, y, z, *args):
        pass


class InnerClassOverride(SuperClass):
    @overrides
    class SomeClass:
        def check(self):
            return 1


class OverridesTests(unittest.TestCase):
    def test_overrides_passes_for_same_package_superclass(self):
        sub = SubClass()
        self.assertEqual(sub.some_method(), "sub")
        self.assertEqual(sub.some_method.__doc__, "Super Class Docs")

    def test_override_inner_class(self):
        sup = SuperClass.SomeClass()
        sub = InnerClassOverride.SomeClass()
        self.assertEqual(sup.check(), 0)
        self.assertEqual(sub.check(), 1)
        self.assertEqual(sup.__doc__, sub.__doc__)

    def test_overrides_does_not_override_method_doc(self):
        sub = Subber()
        self.assertEqual(sub.some_method(), 1)
        self.assertEqual(sub.some_method.__doc__, "Subber")

    def test_overrides_passes_for_superclass_in_another_package(self):
        sub2 = Sub2()
        self.assertEqual(sub2.somewhat_fun_method(), "foo")
        self.assertEqual(sub2.somewhat_fun_method.__doc__, "LULZ")

    def test_assertion_error_is_thrown_when_method_not_in_superclass(self):
        try:

            class ShouldFail(SuperClass):
                @overrides
                def somo_method(self):
                    pass

            raise RuntimeError("Should not go here")
        except TypeError:
            pass

    def test_static_method(self):
        try:

            class StaticMethodOverrideFail(SuperClass):
                @staticmethod
                @overrides
                def this_is_static(k, y, z):
                    pass

            raise RuntimeError("Should not go here")
        except TypeError:
            pass

    def test_can_override_builtin(self):
        x = SubclassOfInt(10)
        self.assertEqual(str(x), "subclass of int")

    def test_overrides_method_from_generic_subclass(self):
        genericsub = SubSubClassOfGeneric()
        self.assertEqual(genericsub.some_method(), 17)
        self.assertEqual(genericsub.some_method.__doc__, "Generic sub class.")

    def test_overrides_check_at_runtime(self):
        with self.assertRaises(TypeError):
            CheckAtRuntime().some_method(1)

    def test_overrides_builtin_method_correct_signature(self):
        class SubclassOfInt(int):
            @overrides
            def bit_length(self):
                return super().bit_length()

        x = SubclassOfInt(1)
        self.assertEqual(x.bit_length(), 1)

    def test_overrides_builtin_method_incorrect_signature(self):
        if sys.version_info >= (3, 7):
            expected_error = self.assertRaises(TypeError)
        else:
            # In 3.6 inspecting signature's isn't possible for builtin
            # methods so this this passes the signature check.
            expected_error = no_error()

        with expected_error:

            class SubclassOfInt(int):
                @overrides
                def bit_length(self, _):
                    "This will fail, bit_length takes in no arguments"


if __name__ == "__main__":
    unittest.main()
