#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import os.path as osp
import sys
import imp
import glob

import yaml


# Helpers
def load_module(filename, condition=None, required=[]):
	"""
	Returns a mapping between all the names defined in the module
	pointed by `filename` and their corresponding values
	"""
	
	if condition is None:
		condition = lambda x: True
	
	# Convention over the module name
	modname = '_task_%s' % osp.splitext(filename)[0]
	
	# Load the module
	try: modobj = imp.load_source(modname, filename)
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
	condition = lambda obj: getattr(obj, 'is_task', False)

	for directory in directories:
		for filename in glob.iglob('%s/*.py' % directory):
			try: names = load_module(filename, condition)
			except Exception, e:
				e.filename = filename
				raise e
			else:
				tasks.update(names)
	return tasks

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


# Main program
if __name__ == '__main__':

	# Find project root
	root = recurse_up(os.getcwd(), 'Cakefile')
	if not root:
		print 'cake aborted!\nNo Cakefile found'
		exit (-1)
	else:
		print "(in %s)" % root

	# Load all tasks
	cakefile = osp.join(root, 'Cakefile')
	with open(cakefile) as f:
		conf = yaml.load(f)
	if not conf: conf = {}

	dirs = conf.get('TASKDIRS')
	if not dirs:
		print 'cake aborted!\nCakefile does not define `TASKDIRS`'
		exit(-1)

	dirs = [osp.join(root, i) for i in dirs]
	try: tasks = load_tasks(dirs)
	except Exception, e:
		print "cake aborted!\n%s: %s" % (e.filename.replace(root + '/', ""), e)
		exit(-1)

	# Check arguments
	if len(sys.argv) <= 1:
		# List all tasks
		width = max([len(i) for i in tasks.keys()] + [30])
		for task in tasks.items():
			print "cake {0:<{2}} # {1}".format(task[0], task[1].desc, width)
	else:
		# Execute task
		taskname   = sys.argv[1]
		args       = [i for i in sys.argv[2:] if i.find('=') == -1]
		kwargs     = dict([i.split('=') for i in sys.argv[2:] if i.find('=') != -1])

		task = tasks.get(taskname)
		if task: task(*args, **kwargs)
		else: print "cake aborted!\nTask '%s' not found" % taskname
