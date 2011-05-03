#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os, sys
import cakelib

# decorators
def task(func):
	func.is_task = true
	return func

# check project cakefile
current = os.getcwd()
while True:
	cakefile = os.path.join(current, 'Cakefile')

	if os.path.exists(cakefile):
		parse = cakelib.load_module(cakefile)
		tasks = cakelib.load_tasks(map(lambda name: os.path.join(current, name), parse['MODULES']))
		print "(in %s)" % current; break

	if current != '/':
		current = os.path.dirname(current)
	else:
		print 'cake aborted!\nNo Cakefile found'
		exit (-1)

# execute task
if len(sys.argv) <= 1:
	print 'cake aborted!\nNo task specified'
	exit(-1)

task   = sys.argv[1]
args   = [i for i in sys.argv[2:] if i.find('=') == -1]
kwargs = dict([i.split('=') for i in sys.argv[2:] if i.find('=') != -1])

tasks[task](*args, **kwargs)
