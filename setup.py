#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

name = 'Mikko Korpela'
# I might be just a little bit too much afraid of those bots..
address = name.lower().replace(' ', '.')+chr(64)+'gmail.com'

setup(name='overrides',
      version='0.5',
      description='A decorator to automatically detect mismatch when overriding a method.',
      author=name,
      author_email=address,
      url='https://github.com/mkorpela/overrides',
      packages=find_packages(),
      license='Apache License, Version 2.0')
