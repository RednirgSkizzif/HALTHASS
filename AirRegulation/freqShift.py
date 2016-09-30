import serial

class freqShift(object):
	
	def __init__(self,port):
		self.ard = serial.Serial(port,9600)
	def changeFreq(f):
		deltaT = 1000/f
		self.ard.write(deltaT
	def close(self):
		self.ard.close()

