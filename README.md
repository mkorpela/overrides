# overrides
A decorator to automatically detect mismatch when overriding a method.
See http://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method

# Installation

    pip install overrides

# Usage

    from overrides import overrides

    class SuperClass(object):

        def method(self):
            """This is the doc for method and will be shown in subclass method too!"""
            return 2

    class SubClass(SuperClass):

        @overrides
        def method(self):
            return 1
