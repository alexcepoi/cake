#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
	name = 'cake',
	version = '0.2.2',

	platforms='linux',
	license = 'GPLv3',

	url = 'https://github.com/alexcepoi/cake',
	download_url = 'https://github.com/alexcepoi/cake/zipball/master',

	description = 'Minimalistic Python build tool inspired by Rake',
	long_description = open('README.rst').read(),

	packages = ['cake'],
	scripts = ['bin/cake'],

	author = 'Alexandru Cepoi',
	author_email = 'alex.cepoi@gmail.com',
	maintainer = 'Alexandru Cepoi',
	maintainer_email = 'alex.cepoi@gmail.com',

	install_requires = ['colorama'],
)

