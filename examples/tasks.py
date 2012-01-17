#! /usr/bin/env python
# -*- coding: utf-8 -*-

from cake.lib import task, path

def common():
	print('current dir: %s' % path.current)
	print('project dir: %s' % path.root)

@task
def task1():
	common()
	print("task1 code executed")

@task("this will override current docstring")
def task2(value):
	""" this is a simple task """
	common()
	print("task2 code executed with value %s" % value)

@task
def task3():
	""" This is a rather long string which is sure to not fit in the terminal width;\nThis example is useful in order to see if the docstring is trimmed like it should be;\nthree dots should be added to the trimmed string and it should fit in one row """
	common()
	print("task3 code executed")
