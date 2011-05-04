Cake is a simple Python-based build program similar to Rake. It uses a
simple yaml file (Cakefile) to load tasks from anywhere in the project.


Requires
---------------------------------------------------
 * PyYAML

Usage
---------------------------------------------------
::

  cake [taskname] [taskargs]

Example
---------------------------------------------------
::

  $ cat Cakefile 
  TASKDIRS: [demo]

  $ cat demo/*.py
  from cake import task

  def common():
  	print 'common code finished'

  @task
  def one():
  	common()
  	print "one finished"

  @task()
  def two():
  	common()
  	print "two finished"

  @task("complex task")
  def three(value):
  	common()
  	print "three finished with value %s" % value

  $ cake
  (in /home/alex/work/python/cake)
  cake one                            # 
  cake three                          # complex task
  cake two                            # 

  $ cake three 2
  (in /home/alex/work/python/cake)
  common code finished
  three finished with value 2

Install
---------------------------------------------------
::

  pip install cake

