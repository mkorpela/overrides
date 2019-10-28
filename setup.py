#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

name = 'Mikko Korpela'
# I might be just a little bit too much afraid of those bots..
address = name.lower().replace(' ', '.')+chr(64)+'gmail.com'

desc = 'A decorator to automatically detect mismatch when overriding a method.'

setup(name='overrides',
      version='2.2',
      description=desc,
      author=name,
      author_email=address,
      url='https://github.com/mkorpela/overrides',
      packages=find_packages(),
      license='Apache License, Version 2.0',
      keywords=['override', 'inheritence', 'OOP'],
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
          ]
      )
