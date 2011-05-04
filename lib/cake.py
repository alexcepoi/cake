#! /usr/bin/env python
# -*- coding: utf-8 -*-

import types

def task(arg = None):
	def decorator(func):
		func._task = True
		func._desc = arg if type(arg) is str else ''
		return func

	if type(arg) == types.FunctionType:
		return decorator(arg)
	else: return decorator
