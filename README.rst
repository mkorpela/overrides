overrides 
========

.. image:: https://api.travis-ci.org/drorasaf/overrides.svg?branch=python3_support
        :target: https://travis-ci.org/drorasaf/overrides

.. image:: https://coveralls.io/repos/drorasaf/overrides/badge.svg?branch=python3_support
        :target: https://coveralls.io/r/drorasaf/overrides

.. image:: https://img.shields.io/pypi/v/overrides.svg
        :target: https://pypi.python.org/pypi/overrides

.. image:: http://pepy.tech/badge/overrides
        :target: http://pepy.tech/project/overrides

A decorator to automatically detect mismatch when overriding a method.
See http://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method

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
            """This is the doc for method and will be shown in subclass method too!"""
            return 2

    class SubClass(SuperClass):

        @overrides
        def method(self):
            return 1
