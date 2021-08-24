#!/usr/bin/env python

import os
import sys
from glob import glob

from setuptools import Extension, setup

import versioneer

if glob("*.pyx"):
    from Cython.Build import cythonize
    module_file_ext = 'pyx'
else:
    module_file_ext = 'cpp'

extensions = []
extra_compile_args = ['-DLIB']
if not sys.platform.startswith('win'):
    extra_compile_args.append('-std=c++11')
extra_link_args = []  # -shared -fPIC
include_dirs = []

extensions.append(Extension(
    "pytopickle",
    glob("pandahouse/*.cpp"),
    include_dirs=[],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c++",
))

if module_file_ext == 'pyx':
    ext_modules = cythonize(extensions, include_path=include_dirs, compiler_directives={'embedsignature': True})
else:
    ext_modules = extensions

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
      ext_modules=ext_modules)
