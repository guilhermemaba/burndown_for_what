#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import burndown_for_what

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = burndown_for_what.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='burndown_for_what',
    version=version,
    description="""Simple django application for generate burndown graphics.""",
    long_description=readme + '\n\n' + history,
    author='Guilherme Luis Maba',
    author_email='guilhermemaba@gmail.com',
    url='https://github.com/guilhermemaba/burndown_for_what',
    packages=[
        'burndown_for_what',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='burndown_for_what',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
