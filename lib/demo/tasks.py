from cake import task

def common():
	print 'common code finished'

@task
def one():
	common()
	print "one finished"

@task()
def two():
	""" task docstring """
	common()
	print "two finished"

@task("complex task")
def three(value):
	common()
	print "three finished with value %s" % value
