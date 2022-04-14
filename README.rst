overrides
=========

.. image:: https://img.shields.io/pypi/v/overrides.svg
  :target: https://pypi.python.org/pypi/overrides

.. image:: http://pepy.tech/badge/overrides
  :target: http://pepy.tech/project/overrides

A decorator that verifies that a method that should override an inherited method actually does, and
that copies the docstring of the inherited method to the overridden method. Since signature 
validation and docstring inheritance are performed on class creation and not on class instantiation, 
this library significantly improves the safety and experience of creating class hierarchies in 
Python without significantly impacting performance. See https://stackoverflow.com/q/1167617 for the
initial inspiration for this library.

Motivation
----------

Python has no standard mechanism by which to guarantee that (1) a method that previously overrode an inherited method
continues to do so, and (2) a method that previously did not override an inherited will not override now.
This opens the door for subtle problems as class hierarchies evolve over time. For example,

1. A method that is added to a superclass is shadowed by an existing method with the same name in a 
   subclass.

2. A method of a superclass that is overridden by a subclass is renamed in the superclass but not in 
   the subclass.

3. A method of a superclass that is overridden by a subclass is removed in the superclass but not in
   the subclass.

4. A method of a superclass that is overridden by a subclass but the signature of the overridden
   method is incompatible with that of the inherited one.

These can be only checked by explicitly marking method override in the code.

Python also has no standard mechanism by which to inherit docstrings in overridden methods. Because 
most standard linters (e.g., flake8) have rules that require all public methods to have a docstring, 
this inevitably leads to a proliferation of ``See parent class for usage`` docstrings on overridden
methods, or, worse, to a disabling of these rules altogether. In addition, mediocre or missing
docstrings degrade the quality of tooltips and completions that can be provided by an editor.

Installation
------------

Compatible with Python 3.6+.

.. code-block:: bash

    $ pip install overrides

Usage
-----

Use ``@overrides`` to indicate that a subclass method should override a superclass method.

.. code-block:: python

    from overrides import overrides

    class SuperClass:

        def foo(self):
            """This docstring will be inherited by any method that overrides this!"""
            return 1

        def bar(self, x) -> str:
            return x

    class SubClass(SuperClass):

        @overrides
        def foo(self):
            return 2

        @overrides
        def bar(self, y) -> int: # Raises, because the signature is not compatible.
            return y

Use ``EnforceOverrides`` to require subclass methods that shadow superclass methods to be decorated 
with ``@overrides``.

.. code-block:: python
 
    from overrides import EnforceOverrides

    class SuperClass(EnforceOverrides):

        def foo(self):
            return 1

    class SubClass(SuperClass):

        def foo(self): # Raises, because @overrides is missing.
            return 2

Use ``@final`` to indicate that a superclass method cannot be overriden.

.. code-block:: python

    from overrides import EnforceOverrides, final

    class SuperClass(EnforceOverrides):

        @final
        def foo(self):
            return 1

    class SubClass(SuperClass):

        @overrides
        def foo(self): # Raises, because overriding a final method is forbidden.
            return 2

Note that ``@classmethod`` and ``@staticmethod`` must be declared before ``@overrides``.

.. code-block:: python

    from overrides import overrides

    class SuperClass:

        @staticmethod
        def foo(x):
            return 1

    class SubClass(SuperClass):

        @staticmethod
        @overrides
        def foo(x):
            return 2


Flags of control
----------------

.. code-block:: python

    # To prevent all signature checks do:
    @overrides(check_signature=False)
    def some_method(self, now_this_can_be_funny_and_wrong: str, what_ever: int) -> "Dictirux":
        pass

    # To do the check only at runtime and solve forward references
    @overrides(check_at_runtime=True)
    def some_other_method(self, ..) -> "SomethingDefinedLater":
        pass

    a.some_other_method() # Kaboom if not SomethingDefinedLater


Contributors
------------

This project exists only through the work of all the people who contribute.

mkorpela, drorasaf, ngoodman90, TylerYep, leeopop, donpatrice, jayvdb, joelgrus, lisyarus, 
soulmerge, rkr-at-dbx, ashwin153, brentyi
