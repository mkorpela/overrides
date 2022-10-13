import sys
import unittest

from overrides.overrides import _get_base_class_names

class MyTestClass(unittest.TestCase):
    def test_base_classing(self):
        assert _get_base_class_names(sys._getframe(0)) == [['sys', '_getframe'], ['_get_base_class_names']]
        assert _get_base_class_names(sys._getframe(1)) == []
        assert _get_base_class_names(sys._getframe(2)) == [['testPartExecutor']]
        assert _get_base_class_names(sys._getframe(3)) == [['run']]
        assert _get_base_class_names(sys._getframe(4)) == [['setattr', '_testcase'], ['setattr', '_testcase', 'name', 'obj', '_testcase']]
