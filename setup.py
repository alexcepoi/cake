#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
	name = 'cake',
	version = '0.1',
	license = 'GPLv3',

	url = 'https://github.com/alexcepoi/cake',
	download_url = 'https://github.com/alexcepoi/cake/zipball/master',

	description = 'Simple python build program',
	long_description = open('README.rst').read(),

	package_dir = {'': 'lib'},
	py_modules = ['cake'],
	scripts = ['lib/cake'],

	platforms='any',
	requires = ['PyYAML'],
	install_requires = ['PyYAML'],

	author = 'Alexandru Cepoi',
	author_email = 'alex.cepoi@gmail.com',
	maintainer = 'Alexandru Cepoi',
	maintainer_email = 'alex.cepoi@gmail.com'
)

