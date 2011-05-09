#! /usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import types
import subprocess as sbp
import shlex
import re

from cake.lib import puts

# def task(func):
# 	""" Task decorator """
# 
# 	params = inspect.formatargspec(*inspect.getargspec(func))
# 	specformat = '{cyan}%s {reset}%s'
# 
# 	func._task = True
# 	func._spec = specformat % (func.func_name, params if params != '()' else '')
# 	func._desc = re.sub('\s+', ' ', inspect.getdoc(func) or '')
# 	return func

def task(arg = None):
	""" Task decorator """

	def decorator(func):
		params = inspect.formatargspec(*inspect.getargspec(func))
		specformat = '{cyan}%s {reset}%s'

		func._task = True
		func._spec = specformat % (func.func_name, params if params != '()' else '')
		func._desc = arg if type(arg) is str else inspect.getdoc(func) or ''
		func._desc = re.sub('\s+', ' ', func._desc)
		return func

	if type(arg) == types.FunctionType:
		return decorator(arg)
	else: return decorator

def sh(command):
	""" Run a shell command """

	puts('{magenta}>>{yellow} %s' % command)
	command = shlex.split(command)
	return sbp.call(command)
