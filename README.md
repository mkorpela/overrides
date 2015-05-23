# overrides
overrides decorator to automatically detect mismatch when overriding a method

# Installation

    pip install overrides

# Usage

    from overrides import overrides

    class SuperClass(object):

        def method(self):
            return 2

    class SubClass(SuperClass):

        @overrides
        def method(self):
            return 1
