#
#  Copyright 2015 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import inspect
import re
__VERSION__ = '0.1'

def overrides(method):
    """Decorator to indicate that the decorated method overrides a method in superclass
    The decorator code is executed while loading class. Using this method should have minimal runtime performance
    implications.

    This is based on my idea about how to do this and fwc:s highly improved algorithm for the implementation
    fwc:s algorithm : http://stackoverflow.com/a/14631397/308189
    my answer : http://stackoverflow.com/a/8313042/308189

    How to use:
    from overrides import overrides

    class SuperClass(object):

        def method(self):
            return 2

    class SubClass(SuperClass):

        @overrides
        def method(self):
            return 1

    :raises  AssertionError if no match
    """
    stack = inspect.stack()
    base_classes = [s.strip() for s in re.search(r'class.+\((.+)\)\s*:', stack[2][4][0]).group(1).split(',')]
    if not base_classes:
        raise ValueError('overrides decorator: unable to determine base class for method "%s"' % method.__name__)
    # replace each class name in base_classes with the actual class type
    derived_class_locals = stack[2][0].f_locals
    for i, base_class in enumerate(base_classes):
        if '.' not in base_class:
            base_classes[i] = derived_class_locals[base_class]
        else:
            components = base_class.split('.')
            # obj is either a module or a class
            obj = derived_class_locals[components[0]]
            for c in components[1:]:
                assert(inspect.ismodule(obj) or inspect.isclass(obj))
                obj = getattr(obj, c)
            base_classes[i] = obj
    if not any(hasattr(cls, method.__name__) for cls in base_classes):
        raise AssertionError('No super class method found for "%s"' % method.__name__)
    return method


if __name__ == '__main__':

    class SuperbDiamondClass(object):

        def my_diamond_method(self):
            pass

    class SuperClassA(SuperbDiamondClass):

        def super_class_method_a(self):
            pass

    class SuperClassB(SuperbDiamondClass):

        def super_class_method_b(self):
            pass

    class InheritedClass(SuperClassA, SuperClassB):

        @overrides
        def super_class_method_a(self):
            return 2

        @overrides
        def super_class_method_b(self):
            return 1

        @overrides
        def my_diamond_method(self):
            return 0

