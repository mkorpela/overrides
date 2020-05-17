overrides 
=========

.. image:: https://api.travis-ci.org/mkorpela/overrides.svg
        :target: https://travis-ci.org/mkorpela/overrides

.. image:: https://coveralls.io/repos/mkorpela/overrides/badge.svg
        :target: https://coveralls.io/r/mkorpela/overrides

.. image:: https://img.shields.io/pypi/v/overrides.svg
        :target: https://pypi.python.org/pypi/overrides

.. image:: http://pepy.tech/badge/overrides
        :target: http://pepy.tech/project/overrides

A decorator to automatically detect mismatch when overriding a method.
See http://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method

All checks are done when a class or a method is created and *not* when a method is executed or
an instance of a class is created. This means that performance implications are minimal.

*Note:*
Version 2.8.0 is the last one that supports Python 2.7.
Versions after that work with Python >= 3.6.

Why explicit overrides?
-----------------------

Overrides without explicit indicator for them are weak. The relation can be staticly checked only against current codebase but
this leaves room for problems that happen during evolution of a codebase.

1. (create) Accidental overriding when adding a method to superclass.
2. (modify) Rename of a superclass method without subclass method rename.
3. (delete) Deleting of a superclass method without detecting in subclass that method is not anymore overriding anything.

These might happen for example when overriding a method in a module that does not live in your codebase, or when merging changes done by someone else to the codebase without having access to your subclass.

Installation
------------
.. code-block:: bash

    $ pip install overrides

Usage
-----
.. code-block:: python

    from overrides import overrides

    class SuperClass(object):

        def method(self):
            """This is the doc for a method and will be shown in subclass method too!"""
            return 2

    class SubClass(SuperClass):

        @overrides
        def method(self):
            return 1


Enforcing usage
---------------

.. code-block:: python


    from overrides import EnforceOverrides, final, overrides

    class SuperClass(EnforceOverrides):

        @final
        def method(self):
            """This is the doc for a method and will be shown in subclass method too!"""
            return 2
        
        def method2(self):
            """This is the doc for a method and will be shown in subclass method too!"""
            return 2
        
        def method3(self):
            """This is the doc for a method and will be shown in subclass method too!"""
            return 2

    # THIS FAILS
    class SubClass1(SuperClass):

        def method(self): # <-- overriding a final method
            return 1

    
    # THIS FAILS
    class SubClass2(SuperClass):

        def method2(self): # <-- @overrides decorator missing
            return 1
            
    # THIS ONE IS OK
    class SubClass3(SuperClass):

        @overrides
        def method2(self):
            return 1



