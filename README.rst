It uses a simple python script (Cakefile) located in the project root to define its task.
The tasks can also be loaded from random locations. Cake can be run from anywhere within the project

Features
---------------------------------------------------
 * Task descriptions
 * Task arguments
 * Colored output

Usage
---------------------------------------------------
::

  cake [taskname] [taskargs]

Example
---------------------------------------------------
::

  $ cat Cakefile 
  self.load('tasks/*.py')

  @task
  def test():
      """ this task does nothing """
      print("this is a test")

::

  $ cat tasks/*.py
  def common():
  	print("common code executed")

  @task
  def task1():
        common()
  	print("task1 code executed")

  @task("this will override current docstring")
  def task2(value):
  	""" this is a simple task """
  	common()
  	print("task2 code executed with value %s" % value)

::

  $ cake
  (in /home/alex/work/cake2/examples)
  cake test                                  # this task does nothing
  cake task1                                 # 
  cake task2 (value)                         # this will override current docstring
        
::

  $ cake task2 hello
  (in /home/alex/work/cake2/examples)
  common code executed
  task2 code executed with value hello

Install
---------------------------------------------------
::

  pip install cake

