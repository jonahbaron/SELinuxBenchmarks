#!/usr/bin/python

import datetime
import os

def copytime(filesrc,filedst):
	t1 = datetime.datetime.now()
	os.system("cp " + filesrc + " copyfile.txt")
	t2 = datetime.datetime.now()
	t3 = t2 - t1

	print "Evaluating " + filesrc	
	os.system("rsync -Wv " + filesrc + " " + filedst + " | grep 'bytes/sec'")
	print "Pre-copy time: ", t1
	print "Post-copy time: ", t2
	print "Difference: ", t3
	print ""

	os.system("rm copyfile.txt")
	return t3

def copyfilesBM():
	print "Copy file benchmark"
	filepath = os.getcwd()

	os.system("dd if=/dev/urandom of=4kbFile.txt bs=4KB count=1 > /dev/null 2>&1")
	f1copy = copytime("4kbFile.txt",filepath)

	os.system("dd if=/dev/urandom of=1kbFile.txt bs=1KB count=1 > /dev/null 2>&1")
	f2copy = copytime("1kbFile.txt",filepath)

	os.system("dd if=/dev/urandom of=256bFile.txt bs=256 count=1 > /dev/null 2>&1")
	f3copy = copytime("256bFile.txt",filepath)

	os.system("rm 4kbFile.txt")
	os.system("rm 1kbFile.txt")
	os.system("rm 256bFile.txt")

	copybenchmarks = [f1copy,f2copy,f3copy]
	return copybenchmarks
	

def pipesBM():
	print "Pipes benchmark"

	os.system("dd if=/dev/urandom of=512bFile.txt bs=512 count=1 > /dev/null 2>&1")	

	pipecmd1 = "cat 512bFile.txt > test.txt"
	pipecmd2 = "cat test.txt > test2.txt"

	t1 = datetime.datetime.now()
	pipe1 = os.system(pipecmd1)
	t2 = datetime.datetime.now()
	pipe2 = os.system(pipecmd2)
	t3 = datetime.datetime.now()
	
	print t1
	print pipecmd1
	print t2
	print pipecmd2
	print t3
	print ""

	t4 = t2 - t1
	t5 = t3 - t1
	
	print "Difference between t2 and t1: ", t4
	print "Difference between t3 and t1: ", t5
	print ""

	os.system("rm 512bFile.txt")
	os.system("rm test.txt")
	os.system("rm test2.txt")

	return t5

def write1(count):
	os.system("echo '" + str(count) + "' >> contextpipes.txt")
	count += 1
	
	if count <= 100:
		write2(count)
	else:
		trash = pipeswitchingBM(count)

def write2(count):
	os.system("echo '" + str(count) + "' >> contextpipes.txt")
	count += 1

	if count <= 100:
		write1(count)
	else:
		trash = pipeswitchingBM(count)

def pipeswitchingBM(count):
	global contextt1
	if count == 0:
		print "Context switching benchmark"
		contextt1 = datetime.datetime.now()
		write1(count)
	else:
		t2 = datetime.datetime.now()
		t3 = t2 - contextt1

		print "Pre-contextswitching time: ", contextt1
		print "Post-contextswitching time: ", t2
		print "Difference: ", t3
		print ""

		os.system("rm contextpipes.txt")
		return t3

def processBM():
	print "Process creation benchmark"

	t1 = datetime.datetime.now()
	
	simpleprocess = os.fork()
	if simpleprocess == 0:
		os._exit(0)
	
	os.waitpid(simpleprocess, 0)

	t2 = datetime.datetime.now()
	t3 = t2 - t1
	
	print "Pre-child time: ", t1
	print "Post-child time: ", t2
	print "Difference: ", t3
	print ""

	return t3

def execlBM():
	print "Execl commands benchmark"

	t1 = datetime.datetime.now()
	
	execlprocess = os.fork()
	if execlprocess == 0:
		os.execl("/usr/bin/python", "python", "-V")
	
	os.waitpid(execlprocess, 0)

	t2 = datetime.datetime.now()
	t3 = t2 - t1

	print "Pre-execl time: ", t1
	print "Post-execl time: ", t2
	print "Difference: ", t3
	print ""

	return t3

def script(count):
	#lock.acquire()
	if count % 2 == 0:
		os.system("perl -pe '$_= lc($_)' file.txt > file.txt")
	elif count % 2 == 1:
		os.system("perl -pe '$_= uc($_)' file.txt > file.txt")
	else:
		print "Error"
	#lock.release()

def concurrentBM():
	print "Concurrent processes benchmark"

	#lock = Lock()
	os.system("dd if=/dev/urandom of=file.txt bs=10KB count=1 > /dev/null 2>&1")
	children = []

	t1 = datetime.datetime.now()
	for process in range(8):
		pid = os.fork()
		if pid:
			children.append(pid)
		else:
			script(process)
			os._exit(0)
	for i, child in enumerate(children):
		os.waitpid(child, 0)

	#script(count)
	#returnvalue = Process(target=script, args=(lock, count)).start()
	t2 = datetime.datetime.now()
	t3 = t2 - t1

	print "Pre-processes: ", t1
	print "Post-processes: ", t2
	print "Difference: ", t3
	print ""

	os.system("rm file.txt")

	return t3

def main():
	print "Unix benchmarks"
	print ""

	benchmarks1 = []
	benchmarks2 = []

	for count in range(2):
		if count == 0:
			os.system("setenforce 0")
		elif count == 1:
			os.system("setenforce 1")
		copyfiles = copyfilesBM()
		pipes = pipesBM()
		pipeswitching = pipeswitchingBM(0)
		process =  processBM()
		execl = execlBM()
		concurrent = concurrentBM()
		
		f1copy = copyfiles[0]
		f2copy = copyfiles[1]
		f3copy = copyfiles[2]
		
		if count == 0:
			benchmarks1 = [f1copy, f2copy, f3copy, pipes, pipeswitching, process, execl, concurrent]
		elif count == 1:
			benchmarks2 = [f1copy, f2copy, f3copy, pipes, pipeswitching, process, execl, concurrent]

	for value in benchmarks1:
		print value
	print ""

	for value in benchmarks2:
		print value
	print ""

	os.system("setenforce 1")
	print "Benchmark finished"


if __name__ == "__main__":
	main()
