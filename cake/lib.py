#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as osp
import re
import sys
import curses
import types
import inspect


class Prototype(object):
	pass

# object used for accessing cake paths
path = Prototype()


def task(arg = None):
	""" Task decorator """

	def decorator(func):
		params = inspect.formatargspec(*inspect.getargspec(func))
		specformat = '{cyan}%s {reset}%s'

		func._task = True
		func._spec = specformat % (func.__name__, params if params != '()' else '')
		func._desc = arg if type(arg) is str else inspect.getdoc(func) or ''
		func._desc = re.sub('\s+', ' ', func._desc)
		return func

	if type(arg) == types.FunctionType:
		return decorator(arg)
	else: return decorator


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


def puts(*args, **kwargs):
	"""
	Prints each argument on a separte line color (highlighted and trimmed for tty)
	"""

	# TODO: generalize
	# trim   = kwargs.get('trim') is not False
	# color  = kwargs.get('color') is not False
	# stream = kwargs.get('stream') or sys.stdout

	# stringify args
	args = [str(i) for i in args]

	# helpers
	Fore = {
			'RESET': '\x1b[0m',
			'BOLD': '\x1b[1m',

			'BLACK': '\x1b[30m',
			'RED': '\x1b[31m',
			'GREEN': '\x1b[32m',
			'YELLOW': '\x1b[33m',
			'BLUE': '\x1b[34m',
			'MAGENTA': '\x1b[35m',
			'CYAN': '\x1b[36m',
			'WHITE': '\x1b[37m',
			}

	def replace(ansi = True):
		def func(mobj):
			color = Fore.get(mobj.group(1).upper())
			if color:
				if ansi: return color
				else: return ''
			else: return mobj.group(0)
		return func

	def trim(ansi, width):
		string = ''; size = 0; i = 0

		while i < len(ansi):
			mobj = re.match('\x1b[^m]*m', ansi[i:])
			if mobj:
				# append ansi code
				string = string + mobj.group(0)
				i += len(mobj.group(0))
			else:
				# loop for more ansi codes even at max width
				size += 1
				if size > width: break

				# append normal char
				string = string + ansi[i]
				i += 1
		return string

	# process strings
	if not sys.stdout.isatty():
		# remove ansi codes and print
		for string in args:
			print(re.sub('{(.+?)}', replace(False), string))
	else:
		# get terminal width
		try: curses.setupterm()
		except: width = float('inf')
		else: width = curses.tigetnum('cols')

		# trim string
		for string in args:
			string =  re.sub('{(.+?)}', replace(True), string)

			trimmed = trim(string, width)
			if len(trimmed) < len(string):
				trimmed = trim(string, width - 3) + '...'
			print(trimmed + Fore['RESET'])
