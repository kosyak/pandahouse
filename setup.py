#!/usr/bin/env python

import os
import sys
from glob import glob

from setuptools import Extension, setup

import versioneer

extra_compile_args = []
if not sys.platform.startswith('win'):
    extra_compile_args.append('-std=c++11')

ext_module = Extension(
    "pytopickle",
    sources=glob("pandahouse/*.cpp"),
    extra_compile_args=extra_compile_args,
    language="c++",
)

setup(name='pandahouse',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Pandas interface for Clickhouse HTTP API',
      url='http://github.com/kszucs/pandahouse',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      license='BSD',
      keywords='',
      packages=['pandahouse'],
      tests_require=['pytest'],
      setup_requires=['pytest-runner'],
      install_requires=['pandas', 'requests', 'toolz'],
      long_description=(open('README.rst').read() if os.path.exists('README.rst') else ''),
      zip_safe=False,
      ext_modules=[ext_module])
