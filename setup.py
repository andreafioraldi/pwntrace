#!/usr/bin/env python

__author__ = "Andrea Fioraldi"
__copyright__ = "Copyright 2017, Andrea Fioraldi"
__license__ = "MIT"
__email__ = "andreafioraldi@gmail.com"

from setuptools import setup

VER = "1.0.0"

setup(
    name='pwntrace',
    version=VER,
    license=__license__,
    description='Use ltrace with pwnlib.tubes.process instances',
    author=__author__,
    author_email=__email__,
    url='https://github.com/andreafioraldi/pwntrace',
    download_url = 'https://github.com/andreafioraldi/pwntrace/archive/' + VER + '.tar.gz',
    package_dir={'pwntrace': 'pwntrace'},
    packages=['pwntrace'],
    install_requires=['pwn']
)
