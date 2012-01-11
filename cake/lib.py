#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as osp
import re
import sys
import curses
import types
import inspect
import getpass

import colorama
colorama.init()


class Prototype(object):
	pass

# object used for accessing cake paths
path = Prototype()

# object used for accessing colors
colors = Prototype()
colors.__dict__.update(colorama.Fore.__dict__)
colors.__dict__.update(dict([('BACK_%s' % key, val) for key, val in colorama.Back.__dict__.iteritems()]))
colors.__dict__.update(colorama.Style.__dict__)


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


def puts(*args, **kwargs):
	"""
	Full feature printing function featuring ansi color codes,
	trimming and padding for both files and ttys
	"""

	# parse kwargs
	color   = kwargs.pop('color', True)
	trim    = kwargs.pop('trim', True)
	padding = kwargs.pop('padding', None)
	stream  = kwargs.pop('stream', sys.stdout)

	# stringify args
	args = [str(i) for i in args]

	# helpers
	def replace(ansi = True):
		def func(mobj):
			color = getattr(colors, mobj.group(1).upper())
			if color:
				if ansi: return color
				else: return ''
			else: return mobj.group(0)
		return func

	def trimstr(ansi, width):
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
		return (string, size)

	# process strings
	if not stream.isatty():
		# remove ansi codes and print
		for string in args:
			stream.write(re.sub('{(\w+?)}', replace(False), string) + '\n')
	else:
		# get terminal width
		try: curses.setupterm()
		except:
			trim = False
			padding = None
		else:
			width = curses.tigetnum('cols')

		for string in args:
			# color string
			string =  re.sub('{(\w+?)}', replace(color), string)

			if trim or padding:
				trimmed, size = trimstr(string, width)

			# trim string
			if trim:
				if len(trimmed) < len(string):
					trimmed = trimstr(string, width - 3)[0] + '...'
				string = trimmed

			# add padding
			if padding:
				string += padding * (width - size)

			# print final string
			stream.write(string + colors.RESET_ALL + '\n')


def sudo(user='root'):
	if getpass.getuser() != user:
		args = ['sudo', '-u%s' % user, sys.executable] + sys.argv
		os.execvpe(args[0], args, os.environ)
