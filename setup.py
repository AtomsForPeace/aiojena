#!/usr/bin/python
# -*- coding: utf-8 -*-
# File name: setup.py

from setuptools import setup


setup(
    name='aiojena',
    version='0.0.4',
    packages=['aiojena'],
    description='A Jena wrapper for aiosparql with automatic type conversion',
    install_requires=['RDFLib', 'aiosparql'],
)
