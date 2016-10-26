import os,time
filename=raw_input('filename:   ')
while 1:
	try:f = open(filename, 'r', os.O_NONBLOCK);print f.readline();f.close()
	except:print ''


