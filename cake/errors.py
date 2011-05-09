#! /usr/bin/env python
# -*- coding: utf-8 -*-

class CakeError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return self.name

