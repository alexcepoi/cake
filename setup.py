#! /usr/bin/python2.6
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
	name = 'cake',
	version = '0.1',
	description = 'Simple python build program',
	requires=['PyYAML'],
	scripts = ['cake'],
	py_modules=['cake']
)

