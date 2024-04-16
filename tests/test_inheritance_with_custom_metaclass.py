from overrides import EnforceOverrides
from overrides.enforce import EnforceOverridesMeta
import unittest


class CustomMetaClass(EnforceOverridesMeta):
    def __new__(metacls, classname, bases, classdict, **kwargs):
        return super().__new__(metacls, classname, bases, classdict, **kwargs)

    @classmethod
    def foo(cls):
        pass

    def bar(self):
        pass


class SuperbClass(EnforceOverrides, metaclass=CustomMetaClass):
    pass


class InheritanceWithCustomMetaclass(unittest.TestCase):
    def test_inheritance_with_EnforceOverrides_and_custom_metaclass(self):
        sc = SuperbClass()
        self.assertIsInstance(sc, SuperbClass)
        self.assertTrue(issubclass(SuperbClass, EnforceOverrides))
