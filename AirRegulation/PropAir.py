import serial 
import minimalmodbus as mm

class PropAir(object):
	
	def __inti__(self,port):
		self.ins = mm.Instrument(port,247)
		self.ins.serial.parity = 'E'
		self.ins.serial.timeout = .160
	
	def setPressure(self,val):
		#mapping to press needs to be fixed
		press = val*100
		self.ins.write_register(49,press)
	
	def readPressure(self):
		return self.ins.read_register(49)/100
