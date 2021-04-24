import unittest
from typing import Union, Optional

from overrides import overrides, final, EnforceOverrides
from overrides.enforce import ensure_signature_is_compatible


class Enforcing(EnforceOverrides):
    classVariableIsOk = "OK?"

    @final
    def finality(self):
        return "final"

    def nonfinal1(self, param: int) -> str:
        return "super1"

    def nonfinal2(self):
        return "super2"

    @property
    def nonfinal_property(self):
        return "super_property"

    @staticmethod
    def nonfinal_staticmethod():
        return "super_staticmethod"

    @classmethod
    def nonfinal_classmethod(cls):
        return "super_classmethod"


class EnforceTests(unittest.TestCase):
    def test_enforcing_when_all_ok(self):
        class Subclazz(Enforcing):
            classVariableIsOk = "OK!"

            @overrides
            def nonfinal1(self, param: int) -> str:
                return 2

        sc = Subclazz()
        self.assertEqual(sc.finality(), "final")
        self.assertEqual(sc.nonfinal1(1), 2)
        self.assertEqual(sc.nonfinal2(), "super2")
        self.assertEqual(sc.classVariableIsOk, "OK!")

    def test_enforcing_when_finality_broken(self):
        try:
            class BrokesFinality(Enforcing):
                def finality(self):
                    return "NEVER HERE"

            raise RuntimeError('Should not go here')
        except AssertionError:
            pass

    def test_enforcing_when_none_explicit_override(self):
        try:
            class Overrider(Enforcing):
                def nonfinal2(self):
                    return "NEVER HERE EITHER"

            raise RuntimeError('Should not go here')
        except AssertionError:
            pass

    def test_enforcing_when_property_overriden(self):
        class PropertyOverrider(Enforcing):
            @property
            @overrides
            def nonfinal_property(self):
                return "subclass_property"

        self.assertNotEqual(PropertyOverrider.nonfinal_property,
                            Enforcing.nonfinal_property)

    def test_enforcing_when_incompatible(self):
        with self.assertRaises(TypeError):
            class Incompatible(Enforcing):
                @overrides
                def nonfinal1(self, param: str):
                    pass

    def test_enforcing_when_staticmethod_overriden(self):
        class StaticMethodOverrider(Enforcing):
            @staticmethod
            @overrides
            def nonfinal_staticmethod():
                return "subclass_staticmethod"

        self.assertNotEqual(
            StaticMethodOverrider.nonfinal_staticmethod(),
            Enforcing.nonfinal_staticmethod(),
        )

    def test_enforcing_when_classmethod_overriden(self):
        class ClassMethodOverrider(Enforcing):
            @classmethod
            @overrides
            def nonfinal_classmethod(cls):
                return "subclass_classmethod"

        self.assertNotEqual(ClassMethodOverrider.nonfinal_classmethod(),
                            Enforcing.nonfinal_classmethod())

    def test_enforcing_when_metaclass_method_overridden(self):
        class MetaClassMethodOverrider(Enforcing):
            def register(self):
                pass

        with self.assertRaises(AssertionError):
            class SubClass(MetaClassMethodOverrider):
                def register(self):
                    pass

    def test_ensure_compatible_when_compatible(self):
        def sup(a, /, b: str, c: int, *, d, e, **kwargs) -> object:
            pass

        def sub(a, b: object, c, d, f: str = "foo", *args, g: str = "bar", e, **kwargs) -> str:
            pass

        ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_type_hints_are_strings(self):        
        def sup(x: "str") -> "object":
            pass

        def sub(x: "object") -> "str":
            pass

        ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_return_types_are_incompatible(self):
        def sup(x) -> int:
            pass

        def sub(x) -> str:
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_parameter_positions_are_incompatible(self):
        def sup(x, y):
            pass

        def sub(y, x):
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_parameter_types_are_incompatible(self):
        def sup(x: object):
            pass

        def sub(y: str):
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_parameter_kinds_are_incompatible(self):
        def sup(x):
            pass

        def sub(*, x):
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_parameter_lists_are_incompatible(self):
        def sup(x):
            pass

        def sub(x, y):
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_missing_arg(self):
        def sup():
            pass

        def sub(x):
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_ensure_compatible_when_additional_arg(self):
        def sup(x):
            pass

        def sub():
            pass

        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sup, sub)

    def test_union_compatible(self):
        def sup(x: int):
            pass

        def sub(x: Union[int, str]):
            pass

        ensure_signature_is_compatible(sup, sub)
        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sub, sup)

    def test_generic_sub(self):
        def better_typed_method(x: int, y: Optional[str], z: float = 3.0):
            pass

        def generic_method(*args, **kwargs):
            pass

        ensure_signature_is_compatible(better_typed_method, generic_method)
        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(generic_method, better_typed_method)

    def test_if_super_has_args_then_sub_must_have(self):
        def sub1(x=2, y=3, z=4, /):
            pass

        def subbest(x=1, /, *burgs):
            pass

        def supah(*args):
            pass

        # supah() => subbest()
        # supah(2) => subbest(2)
        # supah(2,3) => subbest(2,3)
        # supah(*args) => subbest(*args)
        ensure_signature_is_compatible(supah, subbest)

        # sub1(1,2,3) => subbest(1,2,3)
        # sub1() => subbest()
        ensure_signature_is_compatible(sub1, subbest)

        with self.assertRaises(TypeError):
            # supah() => sub1() ok
            # supah(2) => sub1(2) ok
            # supah(1,2,3,4) => sub1() takes from 0 to 3 positional arguments but 4 were given
            ensure_signature_is_compatible(supah, sub1)

        with self.assertRaises(TypeError):
            # subbest() => sub1() ok
            # subbest(1,2,3) => sub1(1,2,3) ok
            # subbest(1,2,3,4) => sub1() takes from 0 to 3 positional arguments but 4 were given
            ensure_signature_is_compatible(subbest, sub1)

    def test_if_super_has_kwargs_then_sub_must_have(self):
        def sub1(*, x=3, y=3, z=4):
            pass

        def sus(*, x=3, **kwargs):
            pass

        def superb(**kwargs):
            pass

        # superb() => sus()
        # superb(foo=1) => sus(foo=1)
        # superb(x=4) => sus(x=4)
        # superb(x=4, foo=1) => sus(x=4, foo=1)
        # superb(**kwargs) => sus(**kwargs)
        ensure_signature_is_compatible(superb, sus)
        ensure_signature_is_compatible(sub1, sus)
        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(superb, sub1)
        with self.assertRaises(TypeError):
            ensure_signature_is_compatible(sus, sub1)

    def test_allowed_extra_args_in_overrider(self):
        def superb():
            pass

        def optional_arg(arg=1):
            pass

        def optional_positional_arg(arg2=2, /):
            pass

        def optional_kw_only_arg(*, arg3=3):
            pass

        # superb() => optional_arg()
        ensure_signature_is_compatible(superb, optional_arg)
        # superb() => optional_positional_arg()
        ensure_signature_is_compatible(superb, optional_positional_arg)
        # superb() => optional_kw_only_arg()
        ensure_signature_is_compatible(superb, optional_kw_only_arg)
