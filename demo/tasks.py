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
def three():
	common()
	print "three finished"
