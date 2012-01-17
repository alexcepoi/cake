#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as osp
import re
import types
import inspect

from cake.color import fore


# object used for accessing cake paths
class ProjectPaths(object):
	__slots__ = ['current', 'root']

path = ProjectPaths()


def task(arg = None):
	""" Task decorator """

	def decorator(func):
		params = inspect.formatargspec(*inspect.getargspec(func))
		specformat = fore.cyan('%s') + fore.white('%s')

		func._task = True
		func._spec = specformat % (func.__name__, params if params != '()' else '')
		func._desc = arg if type(arg) is str else inspect.getdoc(func) or ''
		func._desc = re.sub('\s+', ' ', func._desc)
		return func

	if type(arg) == types.FunctionType:
		return decorator(arg)
	else:
		return decorator


def recurse_up(directory, filename):
	"""
	Recursive walk a directory up to root until it contains `filename`
	"""

	directory = osp.abspath(directory)

	while True:
		searchfile = osp.join(directory, filename)

		if osp.isfile(searchfile):
			return directory

		if directory == '/': break
		else: directory = osp.dirname(directory)
	return False
