#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as osp
import sys
import glob
import inspect

from cake.lib import *
from cake.errors import *

class Application(object):
	def __init__(self):
		# Prepare environment
		self.env   = { 'self': self }
		self.tasks = {}
	
		# Find Project Root
		self.current = os.getcwd()
		self.root    = recurse_up(self.current, 'Cakefile')

		if self.root:
			os.chdir(self.root)
			puts('{yellow}(in %s)' % self.root)
		else:
			raise CakeError('Cakefile not found')

		# Execute Cakefile
		self.load('Cakefile')

		# Load all tasks
		for name, task in self.env.items():
			if getattr(task, '_task', False):
				self.tasks[name] = task

	def run(self, *argv):
		if not argv:
			self.list_tasks()
		else:
			args       = [i for i in argv[1:] if i.find('=') == -1]
			kwargs     = dict([i.split('=') for i in argv[1:] if i.find('=') != -1])

			self.execute(argv[0], *args, **kwargs)

	def load(self, pattern):
		for fname in glob.iglob(pattern):
			src = 'from cake.helpers import *\n' + open(fname).read()
			exec(src, self.env)
	
	def execute(self, name, *args, **kwargs):
		task = self.tasks.get(name)
		if task:
			try: task(*args, **kwargs)
			except TypeError as e:
				raise CakeError(str(e))
		else:
			raise CakeError('Task `%s` not found' % name)
	
	def list_tasks(self):
		width = max([len(i._spec) for i in self.tasks.values()] + [50])
		keys = self.tasks.keys()
		keys.sort()

		for task in [self.tasks[i] for i in keys]:
			puts('cake %-*s # %s' % (width, task._spec, task._desc))

# Main program
def main():
	try:
		app = Application()
		app.run(*sys.argv[1:])
	except CakeError as e:
		puts('{red}cake aborted!', e)

if __name__ == '__main__':
	main()
