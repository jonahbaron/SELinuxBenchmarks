#!/usr/bin/python

from __future__ import division
import datetime
import os

def copytime(filesrc,filedst):
	t1 = datetime.datetime.now()
	os.system("cp " + filesrc + " copyfile.txt")
	t2 = datetime.datetime.now()
	t3 = t2 - t1

#	print "Evaluating " + filesrc
#	print "Pre-copy time: ", t1
#	print "Post-copy time: ", t2
#	print "Difference: ", t3
#	print ""

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
	
#	print t1
#	print pipecmd1
#	print t2
#	print pipecmd2
#	print t3
#	print ""

	t4 = t2 - t1
	t5 = t3 - t1
	
#	print "Difference between t2 and t1: ", t4
#	print "Difference between t3 and t1: ", t5
#	print ""

	os.system("rm 512bFile.txt")
	os.system("rm test.txt")
	os.system("rm test2.txt")

	return t5

def readfile(count):
	f = open("pipeswitching.txt", "r")
	value = int(f.read())
	f.close()

	intvalue = int(value) + 1
	if count < 10:
		writefile(intvalue,count)

def writefile(value,count):
	os.system("echo " + str(value) + " > pipeswitching.txt")
	count += 1
	readfile(count)

def pipeswitchingBM():
	print "Context switching benchmark"
	os.system("echo 0 > pipeswitching.txt")

	t1 = datetime.datetime.now()
	readfile(0)
	t2 = datetime.datetime.now()
	t3 = t2 - t1

#	print "Pre-processes: ", t1
#	print "Post-processes: ", t2
#	print "Difference: ", t3
#	print ""

	os.system("rm pipeswitching.txt")
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
	
#	print "Pre-child time: ", t1
#	print "Post-child time: ", t2
#	print "Difference: ", t3
#	print ""

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

#	print "Pre-execl time: ", t1
#	print "Post-execl time: ", t2
#	print "Difference: ", t3
#	print ""

	return t3

def perlscript(count):
	if count % 2 == 0:
		os.system("perl -pe '$_= lc($_)' file.txt > file.txt")
	elif count % 2 == 1:
		os.system("perl -pe '$_= uc($_)' file.txt > file.txt")
	else:
		print "Error"

def scriptsBM():
	print "Concurrent processes benchmark"

	os.system("dd if=/dev/urandom of=file.txt bs=10KB count=1 > /dev/null 2>&1")
	children = []
	t1 = datetime.datetime.now()

	for process in range(8):
		pid = os.fork()
		if pid:
			children.append(pid)
		else:
			perlscript(process)
			os._exit(0)
	for i, child in enumerate(children):
		os.waitpid(child, 0)

	t2 = datetime.datetime.now()
	t3 = t2 - t1

#	print "Pre-processes: ", t1
#	print "Post-processes: ", t2
#	print "Difference: ", t3
#	print ""

	os.system("rm file.txt")

	return t3

def main():
	print "Unix benchmarks"
	print ""

	benchmarks1 = []
	benchmarks2 = []

	basemarks = []
	semarks = []

	for count in range(100):
		print count
		for count in range(2):
			if count == 0:
				print "SELinux disabled"
				os.system("setenforce 0")
			elif count == 1:
				print "SELinux enabled"
				os.system("setenforce 1")
			copyfiles = copyfilesBM()
			pipes = pipesBM()
			pipeswitching = pipeswitchingBM()
			process =  processBM()
			execl = execlBM()
			scripts = scriptsBM()
			
			f1copy = copyfiles[0]
			f2copy = copyfiles[1]
			f3copy = copyfiles[2]
			
			if count == 0:
				benchmarks1 = [f1copy.microseconds, f2copy.microseconds, f3copy.microseconds, pipes.microseconds, pipeswitching.microseconds, process.microseconds, execl.microseconds, scripts.microseconds]
			elif count == 1:
				benchmarks2 = [f1copy.microseconds, f2copy.microseconds, f3copy.microseconds, pipes.microseconds, pipeswitching.microseconds, process.microseconds, execl.microseconds, scripts.microseconds]
		basemarks.append(benchmarks1)
		semarks.append(benchmarks2)
		print ""

	benchmarks1 = [sum(time)/len(time) for time in zip(*basemarks)]
	benchmarks2 = [sum(time)/len(time) for time in zip(*semarks)]

	print "Raw BaseOS Benchmarks (microseconds)"
	for value in basemarks:
		print value
	print ""

	print "Raw SELinux Benchmarks (microseconds)"
	for value in semarks:
		print value
	print ""

	names = ["File copy 4KB", "File copy 1KB", "File copy 256B", "Pipe", "Pipe switching", "Process creation", "Execl", "Shell scripts(8)"]

	print "BaseOS Benchmark Averages (microseconds)"
	for count in range(8):
		print names[count], " - ",  benchmarks1[count]
	print ""

	print "SELinux Benchmark Averages (microseconds)"
	for count in range(8):
		print names[count], " - ",  benchmarks2[count]
	print ""

	calcs = []
	for count in range(8):
		value = ((benchmarks2[count] - benchmarks1[count]) / benchmarks1[count]) * 100
		calcs.append(value)

	print "Overhead (% change)"
	for count in range(8):
		print names[count], " - ",  calcs[count]
	print ""

	os.system("setenforce 1")
	print "Unix benchmarks complete"

if __name__ == "__main__":
	main()
