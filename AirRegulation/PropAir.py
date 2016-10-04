import serial 
import minimalmodbus as mm

class PropAir(object):
	
	def __init__(self,port,stepsize,steplength,number of steps):
		self.ins = mm.Instrument(port,247)
		self.ins.serial.parity = 'E'
		self.ins.serial.timeout = .160
		self.step_size = step_size
		self.step_length = step_length
		self.number_of_steps = number_of_steps

	def setPressure(self,pressure):
		#mapping to press needs to be fixed
		val = pressure*655
		self.ins.write_register(49,val)
	
	def readPressure(self):
		return self.ins.read_register(49)/655
		
	
	def checkGrms(self)
		# read grms from arduino
		#return grms
