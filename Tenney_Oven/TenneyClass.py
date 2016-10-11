import serial
from arduino import Arduino
import arduino
import decimal
import time
class Tenney(object):

    Temperature_Acceptance = 2
    
    def __init__(self,com,ardport):
        self.chamber = serial.Serial(com,baudrate=9600,timeout=1)
        self.ard = Arduino(ardport)
        
    def close(self):
        self.chamber.close()
        self.ard.comm.close()

    def open(self):
        self.chamber.open()
        self.ard.comm.open()

    def soak(self,sec):
        deltaT = int(sec/3)
        for deltaT in range(1,deltaT):
            time.sleep(1)
            print 'Soaking'
            ntcTemp = self.ard.readNTC()
            print ntcTemp
                    
    def setPoint(self,setpoint):
        self.setpoint = setpoint
        h = str(setpoint)
        d = decimal.Decimal(h)
        l = d.as_tuple().exponent
        if l < -1:
            raise RuntimeError("Decimals beyond the 'tenths' place not allowed in setpoint")
        else:
            x = "= SP1 " + str(setpoint) + "\n"
            self.chamber.write(x)

    def step(self,start,stop,N,T):
        #print '\n here come dat boi'
        if round(N,1) != round(N,0)+0.0:
            raise RuntimeError('Use only integer values for "N"')
        h = start + 0.0
        l = stop + 0.0
        A = self.Temperature_Acceptance
        stepSoak = T*60

        if h < l:
            for i in range(N+1):
                q = l - h
                s = q/N
                d = round(s,1)
                SP = start + i*d
                print 'Adjusting Setpoint to ' + str(SP)
                self.setPoint(SP)
                time.sleep(1)
                ntcTemp = self.ard.readNTC()
                print ntcTemp
                while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    print ntcTemp
                print 'SetPoint Reached'
                self.soak(stepSoak)
    
        elif h > l:
            for i in range(N+1):
                q = h - l
                s = q/N
                d = round(s,1) 
                SP = start - i*d
                print 'Adjusting Setpoint to ' + str(SP)
                self.setPoint(SP)
                time.sleep(1)
                ntcTemp = self.ard.readNTC()
                print ntcTemp
                while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    print ntcTemp
                print 'Setpoint Reached'
                self.soak(stepSoak)
        #print "\n o shit waddup"
        print 'done'

    def cycle(self,start,stop,N,T,cycles):
        for i in range(1,cycles):
            self.step(start,stop,N,T)
            print 'cycle ' + str(i) + ' of ' + str(cycles) + ' is complete'
        #print 'dat boi has cycled away'
        print ' done'
        
        
            
            
        
    
