import serial 
import minimalmodbus as mm

class PropAir(object):
	
	def __init__(self,port):
		self.ins = mm.Instrument(port,247)
		self.ins.serial.parity = 'E'
		self.ins.serial.timeout = .160
		

	def setPressure(self,press):
		#mapping to press needs to be fixed
		val = press*655
		self.ins.write_register(49,val)
	
	def readPressure(self):
		return self.ins.read_register(49)/655
		
	
	def checkGrms(self)
		# read grms from arduino
		#return grms
