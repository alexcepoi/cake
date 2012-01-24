It uses a simple python script (Cakefile) located in the project root to define its tasks.
Cake can be run and can run tasks from anywhere within the project.

Features
---------------------------------------------------
 * Task descriptions
 * Task arguments
 * Colored output

Usage
---------------------------------------------------
List all tasks

::

  cake

Execute task

::

  cake [name] [args]

Example
---------------------------------------------------
::

  $ cat Cakefile 
  from cake.lib import task, path

  @task("header information")
  def test(value='test'):
      """ task description """
      print('current dir: %s' % path.current)
      print('project dir: %s' % path.root)
      print('running with value %s' % value)

::

  $ cake
  (in /home/alex/work/cake/examples)
  cake test                                  # task description

::

  $ cake test example
  (in /home/alex/work/cake/examples)
  ** test: header information
  current dir: /home/alex/work/cake/examples
  project dir: /home/alex/work/cake/examples
  running with value example

Install
---------------------------------------------------
::

  pip install cake
