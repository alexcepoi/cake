#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

import types

def task(arg = ""):
	def decorator(func):
		func.is_task = True
		func.desc = arg if type(arg) is str else ''
		return func

	if type(arg) == types.FunctionType:
		return decorator(arg)
	else: return decorator
