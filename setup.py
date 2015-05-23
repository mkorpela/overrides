#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
from overrides import __VERSION__

name = 'Mikko Korpela'
# I might be just a little bit too much afraid of those bots..
address = name.lower().replace(' ', '.')+chr(64)+'gmail.com'

setup(name='overrides',
      version=__VERSION__,
      description='overrides decorator to automatically detect mismatch when overriding a method.',
      author=name,
      author_email=address,
      url='https://github.com/mkorpela/overrides',
      packages=find_packages(),
      license='Apache License, Version 2.0')
