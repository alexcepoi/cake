#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from cake.lib import path, recurse_up
from cake.color import puts, fore
from cake.errors import CakeError


class Application(object):
	def __init__(self):
		# Find Project Root
		path.current = os.getcwd()
		path.root    = recurse_up(path.current, 'Cakefile')

		if path.root:
			os.chdir(path.root)
			sys.path.insert(0, '')

			# Print project path
			puts(fore.yellow('(in %s)' % path.root))
		else:
			raise CakeError('Cakefile not found')

		# Prepare environment
		self.env   = {}
		self.tasks = {}
	
		# Read Cakefile
		with open('Cakefile') as f:
			exec(f.read(), self.env)

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

			self.run_task(argv[0], *args, **kwargs)

	def run_task(self, name, *args, **kwargs):
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
			puts('cake %-*s # %s' % (width, task._spec, task._desc), trim=True)

# Main program
def main():
	try:
		app = Application()
		app.run(*sys.argv[1:])
	except CakeError as e:
		puts(fore.red('cake aborted!\n') + str(e), stream=sys.stderr)

if __name__ == '__main__':
	main()
