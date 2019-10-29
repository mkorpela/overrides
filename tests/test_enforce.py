import unittest
from overrides import overrides,final,EnforceOverrides

class Enforcing(EnforceOverrides):

    @final
    def finality(self):
        return "final"

    def nonfinal1(self):
        return "super1"

    def nonfinal2(self):
        return "super2"

class EnforceTests(unittest.TestCase):

    def test_enforcing_when_all_ok(self):
        class Subclazz(Enforcing):
            @overrides
            def nonfinal1(self):
                return 1
        sc = Subclazz()
        self.assertEqual(sc.finality(), "final")
        self.assertEqual(sc.nonfinal1(), 1)
        self.assertEqual(sc.nonfinal2(), "super2")

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

