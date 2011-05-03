#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import os.path as osp
import sys
import glob
import imp
import py_compile


def load_module(filename, condition=None, required=[]):
	"""
	Returns a mapping between all the names defined in the module
	pointed by `filename` and their corresponding values
	"""
	
	if condition is None:
		condition = lambda x: True
	
	# Convention over the module name
	modname = '_task_%s' % osp.splitext(osp.basename(filename))[0]
	
	# Compile the source in a temporary location
	compfile = filename + 'c'
	
	try:
		py_compile.compile(file=filename, cfile=compfile, doraise=True)
	except py_compile.PyCompileError, e:
		# Translate potential SyntaxError data
		if e.args[0].startswith('SyntaxError'):
			raise SyntaxError(*e.args[2])
		else:
			raise e
	
	# Cleanup old module object
	if modname in sys.modules:
		del sys.modules[modname]
	
	# Load the compiled module
	try:
		modobj = imp.load_compiled(modname, compfile)
	except Exception, e:
		# TODO encapsulate the line with problems in a custom exception
		# and prepare subsequent code to handle it
		raise e
	
	# Dump the list of public names
	namelist = filter(lambda s: not s.startswith('_'), dir(modobj))
	
	# Check the required names defined in config
	for name in required:
		if name not in namelist:
			raise ValueError("module '%s' does not define '%s'" % (modname, name))
	
	# Collect the public names into a namespace and return
	namespace = {}
	for name in namelist:
		obj = getattr(modobj, name)
		if condition(obj):
			namespace[name] = obj
	
	return namespace


def load_tasks(directories):
	"""
	Returns a mapping of all the tasks loaded from all the .py files
	from all the directories (in the `directories` list)
	"""
	
	tasks = {}
	for directory in directories:
		for filename in glob.iglob('%s/*.py' % directory):
			names = {}
			try:
				condition = lambda obj: getattr(obj, 'is_task', False)
				names = load_module(filename, condition)
			except Exception, e:
				print "Can't load %s" % filename
			
			tasks.update(names)
	return tasks


# decorators
def task(func):
	func.is_task = true
	return func


# check project cakefile
current = os.getcwd()
while True:
	cakefile = os.path.join(current, 'Cakefile')

	if os.path.exists(cakefile):
		parse = load_module(cakefile)
		tasks = load_tasks(map(lambda name: os.path.join(current, name), parse['MODULES']))
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
