#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as osp
import sys
import re
import types
import inspect

from cake.color import fore, puts


# object used for accessing cake paths
class ProjectPaths(object):
	__slots__ = ['current', 'root']

path = ProjectPaths()


# indented file
class IndentedFile(object):
	def __init__(self, fobj, indent_level=-1, indent_per_level=2):
		self.fobj = fobj
		self.indent_level = indent_level
		self.indent_per_level = indent_per_level
	
	@property
	def indent(self):
		return max(0, self.indent_level * self.indent_per_level)

	def write(self, *args, **kwargs):
		self.fobj.write(' ' * self.indent)
		self.fobj.write(*args, **kwargs)

	def __getattr__(self, key):
		return getattr(self.fobj, key)


# helpers
def task(arg = None):
	""" Task decorator """

	# make sure stdout is patched
	if not hasattr(sys.stdout, 'indent_level'):
		sys.stdout = IndentedFile(sys.stdout)

	def decorator(base):
		info = ': ' + arg if type(arg) is str else ''
		header = fore.green('** ' + fore.cyan(base.__name__) + info)

		def func(*args, **kwargs):
			sys.stdout.indent_level += 1

			puts(header)
			base(*args, **kwargs)

			sys.stdout.indent_level -= 1

		params = inspect.formatargspec(*inspect.getargspec(base))[1:-1]
		specformat = fore.cyan('%s') + ' ' + fore.white('%s')

		func._task = True
		func._spec = specformat % (base.__name__, params)
		func._desc = re.sub('\s+', ' ', inspect.getdoc(base) or '')
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
