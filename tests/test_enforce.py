from typing import Dict

import unittest
from overrides import overrides,final,EnforceOverrides


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
            def nonfinal1(self, param: int) -> int:
                return 2

        sc = Subclazz()
        self.assertEqual(sc.finality(), "final")
        self.assertEqual(sc.nonfinal1(1), 2)
        self.assertEqual(sc.nonfinal2(), "super2")
        self.assertEqual(sc.classVariableIsOk, "OK!")

    def tests_enforcing_when_finality_broken(self):
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
