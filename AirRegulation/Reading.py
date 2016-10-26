import os,time

def getGrms(filname):
	while 1:
		try:f = open(filename, 'r', os.O_NONBLOCK);val= f.readline();f.close();return float(val)
		except:print ''


