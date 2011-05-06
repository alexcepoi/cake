from cake import task

def common():
	print "common code finished"

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

@task("a rather long boring and complex description that is sure not to fit in the terminal width;\nthis is just an example in order to see if the description will be truncated as they should be;\nthis description should be truncated and end with `...`")
def four(i, n, *args, **kwargs):
	common()
	print "four finished"
