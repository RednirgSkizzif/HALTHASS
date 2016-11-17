import serial 
import minimalmodbus as mm
import time
import Reading as g
rmsFile = "gfile.txt"
        
class Cylinders(object):
        def __init__(self,Cport):
                self.ard = serial.Serial(Cport,9600)
	def changeFreq(self,frequency):
                if (frequency>50):
                        print "TOOFAST"
                        return

                deltaT = 500/frequency
		print deltaT
		time.sleep(1)
		self.ard.flush()
		self.ard.write(str(deltaT))
        def close(self):
                self.ard.close()


class PropAir(object):
        
                def __init__(self,PAport,grmsArduinoPort='none'):
                        self.ins = mm.Instrument(PAport,247)
                        self.ins.serial.parity = 'E'
                        self.ins.serial.timeout = .160
                        self.ins.serial.baudrate = 19200
                        #Lines added by Dylan for the grms read
                        if grmsArduinoPort != 'none' :
                                self.rmsReader = serial.Serial(grmsArduinoPort,9600)
                                self.rmsReader.timeout = 2


                def setPressure(self,pressure):
                        val = pressure*655 #pressure is scaled by a fixed value to map to presure regulator
                        self.ins.write_register(49,val)
			
        
                def readPressure(self):
                        return self.ins.read_register(49)/655
                
                def checkGrms(self):
                        try:
                                dum = float(self.rmsReader.readline().strip())
                        except ValueError:
                                print("Data Fragment Dropped")
                        try:
                                val = float(self.rmsReader.readline().strip())
                        except ValueError:
                                print("Format Error")
                                self.rmsReader.reset_input_buffer()
                                val = checkGrms()
                        self.rmsReader.reset_input_buffer()
                        return val
		
                        
class VibrationCycling(PropAir, Cylinders):
        def __init__(self, PAport, Cport, grmsPort='none'):
                PropAir.__init__(self, PAport, grmsArduinoPort=grmsPort)
                Cylinders.__init__(self, Cport)
	
	def setGrms(self, Grms, length):
		self.Grms = Grms
		self.length = t
		
		pressure = 1			
		t_end = time.time() + (60 * t)
                while time.time() < t_end:
			x = g.getGrms(rmsFile)
			#Check USBPix Flags
			if (( x < (Grms - 1)) and (x > (Grms - 3))):
				pressure = pressure +1
				if pressure > 80:
					pressure = 80
				self.setPressure(pressure)
				time.sleep(1)
			elif ((x > (Grms + 1)) and (x < (Grms + 3))):
				pressure = pressure - 1
				if pressure < 1:
					pressure = 1
				self.setPressure(pressure)
				time.sleep(1)
			elif ((x > (Grms + 3))):
				pressure = pressure -3
				if pressure < 1:
					pressure = 1
				self.setPressure(pressure)
				time.sleep(1)
			elif ((x < (Grms - 3))):
				pressure = pressure + 3
				if pressure > 80:
					pressure = 80
				self.setPressure(pressure)
				time.sleep(1)
			elif ((x >= (Grms - 1)) and (X <= (Grms + 1))):
				time.sleep(1)
				x = g.getGrms(rmsFile)
				print x
				
	def CalibCycle(self, frequency):
		self.changeFreq(frequency)
		
		for n in range(1,36):
			if n < 22:
				self.setPressure(9.5 + (n*.5))
				time.sleep(50)
			elif n >= 22: 
				self.setPressure(n - 1)
				time.sleep(50)
		self.setPressure(0)
		print 'Calibration cycle is complete.'
		
			

        def cycle(self, step_size, start_grms, step_length, number_of_steps, frequency=5):
                self.step_size = step_size
		self.start_grms = start_grms
                self.step_length = step_length
                self.number_of_steps = number_of_steps
                self.changeFreq(frequency)
		pressure = 13
        	for n in range(0,number_of_steps):
                        
                        print 'this is cycle ' + str(n+1)
                        t_end = time.time() + (60 * step_length)
                        while time.time() < t_end:
                                x = g.getGrms(rmsFile)
                                print x
                                # Check USBPIX flags
                                print 'd1'
                                if((x < (start_grms + (n*step_size - .5))) and (x > (start_grms + (n*step_size-1)))):
                                        print 'd2'
                                        pressure = pressure + .05
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif((x > (start_grms + (n*step_size+.5)))  and (x < (start_grms + (n*step_size+1)))):
                                        print 'd3'
                                        pressure = pressure - .20
                                        if pressure < 1:
                                                pressure=1 
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif(x > (start_grms + (n*step_size +1))):
                                        print 'd4'
                                        pressure = pressure - .4
                                        if pressure < 1:
                                                pressure=1  
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                elif(x < (start_grms + (n*step_size - 1))):
                                        print 'd5'
                                        pressure = pressure + .15
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
				elif((x >= (start_grms + (n * step_size - .5))) and (x <= (start_grms + (n * step_size - .2)))):
					print 'd7'
                                        pressure = pressure + .015
                                        if pressure > 80:
                                                pressure = 80
                                        self.setPressure(pressure)
                                        time.sleep(1)
				elif((x <= (start_grms + (n * step_size + .5))) and (x >= (start_grms + (n * step_size + .2)))):
					print 'd8'
                                        pressure = pressure - .075
                                        if pressure < 1:
                                                pressure = 1
                                        self.setPressure(pressure)
                                        time.sleep(1)
                                # Check USBPIX flags
                                elif ((x >= (start_grms + (n * step_size - .2))) and (x <= (start_grms + (n * step_size + .2)))):
                                        print 'd6'
					time.sleep(1)
                                        x = g.getGrms(rmsFile)
                                        print x
                                        
		self.setPressure(0)
                print 'done'
