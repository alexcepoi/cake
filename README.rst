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
  import subprocess as sbp

  from cake.lib import task, path, puts

  @task("description override")
  def test():
      """ task description """
      print('current dir: %s' % path.current)
      print('project dir: %s' % path.root)

  @task
  def shell(value):
      """ execute a custom shell command """
      puts('{magenta}>>{yellow} %s' % value)
      sbp.call(value, shell=True)

::

  $ cake
  (in /home/alex/work/cake/examples)
  cake shell                                 # execute a custom shell command
  cake test                                  # description override

::

  $ cake shell "date"
  (in /home/alex/work/cake/examples)
  >> date
  Thu Jul 21 20:15:37 EEST 2011

Install
---------------------------------------------------
::

  pip install cake
