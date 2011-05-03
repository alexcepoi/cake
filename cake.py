#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

def task(func):
	func.is_task = True
	return func
