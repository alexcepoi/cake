#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import curses
import inspect

import colorama
colorama.init()

ANSI_PATTERN = '\x1b[^m]*m'


class ColorWrapper(object):
	""" Wraps a string in a color or returns color """
	def __init__(self, color):
		self.color = color

	def __str__(self):
		return self.color

	def __call__(self, *args):
		reset  = colorama.Style.RESET_ALL
		string = self.color
		
		for arg in args:
			string += str(arg)

		return string.replace(reset, reset + self.color) + reset


class ColorHelper(object):
	""" Namespace of ColorWrappers """

	def __init__(self, opts):
		self.opts = opts
	
	def __getattr__(self, key):
		if key == key.lower():
			key = key.upper()
			if key in self.opts:
				return ColorWrapper(self.opts[key])

		return super(ColorHelper, self).__getattr__(key)

fore  = ColorHelper(colorama.Fore.__dict__)
back  = ColorHelper(colorama.Back.__dict__)
style = ColorHelper(colorama.Style.__dict__)


def ansi(string, *args):
	""" Convenience function to chain multiple ColorWrappers to a string """

	ansi = ''

	for arg in args:
		arg = str(arg)
		if not re.match(ANSI_PATTERN, arg):
			raise ValueError('Additional arguments must be ansi strings')

		ansi += arg
	
	return ansi + string + colorama.Style.RESET_ALL


def puts(*args, **kwargs):
	"""
	Full feature printing function featuring
	trimming and padding for both files and ttys
	"""

	# parse kwargs
	trim    = kwargs.pop('trim', False)
	padding = kwargs.pop('padding', None)
	stream  = kwargs.pop('stream', sys.stdout)

	# HACK: check if stream is IndentedFile
	indent = getattr(stream, 'indent', 0)

	# stringify args
	args = [str(i) for i in args]

	# helpers
	def trimstr(ansi, width):
		string = ''; size = 0; i = 0

		while i < len(ansi):
			mobj = re.match(ANSI_PATTERN, ansi[i:])
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
			stream.write(re.sub(ANSI_PATTERN, '', string) + '\n')
	else:
		# get terminal width
		try: curses.setupterm()
		except:
			trim = False
			padding = None
		else:
			width = curses.tigetnum('cols') - indent

		for string in args:
			if trim or padding:
				trimmed, size = trimstr(string, width)

			# trim string
			if trim:
				if len(trimmed) < len(string):
					trimmed = trimstr(string, width - 3)[0] + colorama.Style.RESET_ALL + '...'
				string = trimmed

			# add padding
			if padding:
				string += padding * (width - size)

			# print final string
			stream.write(string + '\n')


if __name__ == '__main__':
	print fore.red('red') + style.bright('bold')
	print fore.red('red' + style.bright('bold') + 'red')
	print ansi('redbold', fore.red, style.bright)
	puts(fore.red('red'), padding='=')
	puts(fore.red('red') * 200, trim=True)
