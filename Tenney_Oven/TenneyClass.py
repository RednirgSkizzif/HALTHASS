import serial
from ArduinoClass import Arduino
import decimal
import time
import matplotlib.pyplot as plt
import smtplib
class Tenney(object):

    Temperature_Acceptance = 10

    
    def __init__(self,com,ardport):
        self.chamber = serial.Serial(com,baudrate=9600,timeout=1)
        self.ard = Arduino(ardport)

    def close(self):
        self.chamber.close()
        self.ard.comm.close()

    def open(self):
        self.chamber.open()
        self.ard.comm.open()

    def sendEmail(self):
        s = smtplib.SMTP('smtp-mail.outlook.com',587)
        s.starttls()
        s.login('tenney_chamber@outlook.com','Phase2_upgrade')
        s.ehlo()
        
        try:
            s.sendmail('tenney_chamber@outlook.com',['dylan.frizzell@ou.edu','Trenton.A.Voth-1@ou.edu','abbott@ou.edu','john.stupak@ou.edu'],"Thermal Chamber Error REAL")
            print "email send success"
        except:
            print "email send failure"
        s.quit()
        
        

    def MessedUp(self):
        print "Sending Email"
        self.sendEmail()
        self.ard.comm.close()
        time.sleep(1)
        try:
            self.ard.comm.open()
        except:
            print "Major error. Shutdown."
            self.setPoint(20)
            self.ard.comm.close()
            time.sleep(1)
            self.ard.comm.open()
            print self.ard.comm
            self.ard.readNTC()
        #self.close()

    def soak(self,sec):
        deltaT = int(sec/3)
        for deltaT in range(1,deltaT):
            time.sleep(1)
            print 'Soaking'
            ntcTemp = self.ard.readNTC()
            print ntcTemp
        time.sleep(1)
                    
    def setPoint(self,setpoint):
        self.setpoint = setpoint
        h = str(setpoint)
        d = decimal.Decimal(h)
        l = d.as_tuple().exponent
        if l < -1:
            raise RuntimeError("Decimals beyond the 'tenths' place not allowed in setpoint")
        else:
            x = "= SP1 " + str(setpoint) + "\n"
            try:
                self.chamber.write(x)
            except:
                print "Missed Setpoint Handshake"
                self.sendEmail()
                self.close()
                time.sleep(1)
                self.open()
                

    def step(self,start,stop,N,T):
        f = open("tenney_datalog.csv","a")
        if round(N,1) != round(N,0)+0.0:
            raise RuntimeError('Use only integer values for "N"')
        h = start + 0.0
        l = stop + 0.0
        A = self.Temperature_Acceptance
        stepSoak = T*60
        TempData = []
        starttime = time.time()
        Time = []
        sp = []
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
                TempData.append(ntcTemp)
                Time.append(starttime-time.time())
                sp.append(SP)
                print ntcTemp
                while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    print ntcTemp
                    TempData.append(ntcTemp)
                    Time.append(starttime-time.time())
                    sp.append(SP)
                print 'SetPoint Reached'
                self.soak(stepSoak)
                time.sleep(1)
                
                
    
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
                TempData.append(ntcTemp)
                Time.append(starttime-time.time())
                sp.append(SP)
                print ntcTemp
                while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    TempData.append(ntcTemp)
                    Time.append(starttime-time.time())
                    sp.append(SP)
                    print ntcTemp
                print 'Setpoint Reached'
                self.soak(stepSoak)
        print 'done'
        for i in range(1,len(TempData)):
            try:
                x = str(TempData[i])
                y = str(Time[i]*-1)
            except ValueError:
                print("ValueError")
                x = str(TempData[i+1])
                y = str(Time[i+1]*-1)
            f.write("\n{} , {}".format(x,y))
        f.close()
        #plt.plot(TempData,Time,'ro')
        #plt.show()

    def cycle(self,start,stop,N,T,cycles):
        starttime = time.time()
        stepSoak = T*60
        
        sp = []
        for i in range(1,cycles+1):
            TempData = []
            Time = []
            if round(N,1) != round(N,0)+0.0:
                raise RuntimeError('Use only integer values for "N"')
            h = start + 0.0
            l = stop + 0.0
            A = self.Temperature_Acceptance
            if h < l:
                for p in range(N+1):
                    q = l - h
                    s = q/N
                    d = round(s,1)
                    SP = start + p*d
                    print 'Adjusting Setpoint to ' + str(SP)
                    self.setPoint(SP)
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    if (ntcTemp < -272):
                        self.MessedUp()
                    TempData.append(ntcTemp)
                    Time.append(starttime-time.time())
                    sp.append(SP)
                    print ntcTemp
                    while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                        time.sleep(1)
                        print 'Adjusting Setpoint to ' + str(SP)
                        self.setPoint(SP)
                        ntcTemp = self.ard.readNTC()
                        if (ntcTemp < -272):
                            self.MessedUp()
                        print ntcTemp
                        TempData.append(ntcTemp)
                        Time.append(starttime-time.time())
                        sp.append(SP)
                    print 'SetPoint Reached'
                    self.soak(stepSoak)
                
                
    
            elif h > l:
                for p in range(N+1):
                    q = h - l
                    s = q/N
                    d = round(s,1) 
                    SP = start - p*d
                    print 'Adjusting Setpoint to ' + str(SP)
                    self.setPoint(SP)
                    time.sleep(1)
                    ntcTemp = self.ard.readNTC()
                    if (ntcTemp < -272):
                        self.MessedUp()
                    TempData.append(ntcTemp)
                    Time.append(starttime-time.time())
                    sp.append(SP)
                    print ntcTemp
                    while (ntcTemp > (SP+A)) or (ntcTemp < (SP-A)):
                        time.sleep(1)
                        print 'Adjusting Setpoint to ' + str(SP)
                        self.setPoint(SP)
                        ntcTemp = self.ard.readNTC()
                        if (ntcTemp < -272):
                            self.MessedUp()
                        TempData.append(ntcTemp)
                        Time.append(starttime-time.time())
                        sp.append(SP)
                        print ntcTemp
                    print 'Setpoint Reached'
                    self.soak(stepSoak)
            print 'done'
            for n in range(1,len(TempData)):
                try:
                    x = str(TempData[n])
                    y = str(Time[n]*-1)
                except ValueError:
                    print("ValueError")
                    x = str(TempData[n+1])
                    y = str(Time[n+1]*-1)
                f = open("tenney_datalog.csv","a")
                try:
                    f.write("\n{} , {}".format(x,y))
                except:
                    self.MessedUp()
            f.close()
            #plt.plot(TempData,Time,'ro')
            #plt.show()
            print 'cycle ' + str(i) + ' of ' + str(cycles) + ' is complete'
            print ' done'
            self.setPoint(25)
        
        
            
            
        
    
