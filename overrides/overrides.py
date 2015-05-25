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
__VERSION__ = '0.3'


def overrides(method):
    """Decorator to indicate that the decorated method overrides a method in superclass.
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

    :raises  AssertionError if no match in super classes for the method name
    :return  method with possibly added (if the method doesn't have one) docstring from super class
    """
    for super_class in _get_base_classes(inspect.stack()[2]):
        if hasattr(super_class, method.__name__):
            if not method.__doc__:
                method.__doc__ = getattr(super_class, method.__name__).__doc__
            return method
    raise AssertionError('No super class method found for "%s"' % method.__name__)


def _get_base_classes(class_stack_element, namespace):
    base_class_names = [s.strip() for s in
                        re.search(r'class.+\((.+)\)\s*:',
                                  class_stack_element[4][0]).group(1).split(',')]
    if not base_class_names:
        raise ValueError('overrides decorator: unable to determine base class')
    return [_get_base_class(class_name, namespace) for class_name in base_class_names]


def _get_base_class(class_name, namespace):
    components = class_name.split('.')
    obj = namespace[components[0]]
    for component in components[1:]:
        obj = getattr(obj, component)
    return obj
