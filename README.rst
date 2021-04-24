overrides
=========

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

Overrides without explicit indicator for them are weak. They leave room for problems that happen during the evolution of a codebase.

1. (create) Accidental overriding in a subclass when a method to a superclass is added (or vice versa).
2. (modify) Rename of a superclass method without subclass method rename (or vice versa).
3. (delete) Deleting of a superclass method without detecting in subclass that the method is not anymore overriding anything (or vice versa).

These might happen for example when overriding a method in a module that does not live in your codebase, or when merging changes done by someone else to the codebase without having access to your subclass.

Installation
------------
.. code-block:: bash

    $ pip install overrides

Usage
-----
.. code-block:: python

    from overrides import overrides

    class SuperClass:

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

        @staticmethod
        def method3():
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


    # ENSURE THAT @classmethod AND @staticmethod ARE PLACED AT THE TOP
    class SubClass4(SuperClass):

        @staticmethod
        @overrides
        def method3():
            return 1
 
Contributors
------------
This project becomes a reality only through the work of all the people who contribute.

mkorpela, drorasaf, ngoodman90, TylerYep, leeopop, donpatrice, jayvdb, joelgrus, lisyarus, soulmerge, rkr-at-dbx, ashwin153
