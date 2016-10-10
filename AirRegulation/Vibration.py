import serial 
import minimalmodbus as mm
import time

	
class Cylinders(object):
	def __init__(self,Cport,Cbaud):
		self.ard = serial.Serial(Cport,Cbaud)
	def changeFreq(self,f):
		if (f>50):
			print "TOOFAST"
			return

		deltaT = 1000/f
		self.ard.write(str(deltaT))
	def close(self):
		self.ard.close()


class PropAir(object):
	
		def __init__(self,PAport,step_size,step_length,number_of_steps,grmsArduinoPort='none'):
			self.ins = mm.Instrument(PAport,247)
			self.ins.serial.parity = 'E'
			self.ins.serial.timeout = .160
			self.ins.serial.baudrate = 19200
			self.step_size = step_size #This should be given in grms
			self.step_length = step_length #This should be given in minutes
			self.number_of_steps = number_of_steps
			#Lines added by Dylan for the grms read
			if grmsArduinoPort != 'none' :
				self.rmsReader = serial.Serial(grmsArduinoPort,9600)
				self.rmsReader.timeout = 2


		def setPressure(self,pressure):
			#mapping to press needs to be fixed
			val = pressure*655
			self.ins.write_register(49,val)
	
		def readPressure(self):
			return self.ins.read_register(49)/655
		
	
		def checkGrms(self):
			#time.sleep(0.5)
			try:
			 dum = float(self.rmsReader.readline().strip())
			except ValueError:
			 print("Data Fragment Dropped")
			val = float(self.rmsReader.readline().strip())
			self.rmsReader.reset_input_buffer()
			return val
			# read grms from arduino
			#return grms

			
class VibrationTest(PropAir, Cylinders):
	def __init__(self, PAport, stepsize, steplength, number_of_steps, Cport, Cbaud,grmsPort='none'):
		PropAir.__init__(self, PAport, stepsize, steplength, number_of_steps,grmsArduinoPort=grmsPort)
		Cylinders.__init__(self, Cport, Cbaud)
		
