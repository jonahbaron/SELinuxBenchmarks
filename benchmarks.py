#!/usr/bin/python

import datetime
#import socket
import os

def copytime(filesrc,filedst):
	t1 = datetime.datetime.now()
	os.system("cp " + filesrc + " copyfile.txt")
	t2 = datetime.datetime.now()
	t3 = t2 - t1

	print "Evaluating " + filesrc	
	os.system("rsync -rtv " + filesrc + " " + filedst + " | grep 'bytes/sec'")
	print "Pre-copy time: " + str(t1)
	print "Post-copy time: " + str(t2)
	print "Difference: " + str(t3)
	print ""

	os.system("rm copyfile.txt")

def copyfilesBM():	
	#file = open(filesrc, "rb")
	#blocksize = os.path.getsize(filesrc)
	#sock = socket.socket()
	#sock.connect(("127.0.0.1", 8021))
	#os.sendfile(filesrc, filedst, 0, blocksize)		
	
	print "Copy file benchmark"

	filepath = os.getcwd()	

	os.system("dd if=/dev/zero of=4kbFile.txt bs=4KB count=1 > /dev/null 2>&1")
	copytime("4kbFile.txt",filepath)

	os.system("dd if=/dev/zero of=1kbFile.txt bs=1KB count=1 > /dev/null 2>&1")
	copytime("1kbFile.txt",filepath)

	os.system("dd if=/dev/zero of=256bFile.txt bs=256 count=1 > /dev/null 2>&1")
	copytime("256bFile.txt",filepath)

	os.system("rm 4kbFile.txt")
	os.system("rm 1kbFile.txt")
	os.system("rm 256bFile.txt")
	

def pipesBM():
	print "Pipes benchmark"

	os.system("dd if=/dev/zero of=512bFile.txt bs=512 count=1 > /dev/null 2>&1")	

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
	
	print "Difference between t2 and t1: " + str(t4)
	print "Difference between t3 and t1: " + str(t5)
	print ""

	os.system("rm 512bFile.txt")
	os.system("rm test.txt")
	os.system("rm test2.txt")

def child():
	print "Child process - " + str(os.getpid())
	os._exit(0)

def parentBM():
	print "Process creation benchmark"

	t1 = datetime.datetime.now()
	newprocess=os.fork()
	if newprocess == 0:
		child()
	else:
		print "Parent process - " + str(os.getpid())
	t2 = datetime.datetime.now()
	t3 = t2 - t1
	
	print "Pre-child time: " + str(t1)
	print "Post-child time: " + str(t2)
	print "Difference: " + str(t3)
	print ""

copyfilesBM()
pipesBM()
parentBM()
