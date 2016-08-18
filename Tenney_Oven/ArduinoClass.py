import serial
import time
class Arduino(object):
    s = 0
    x = 0
    
    import serial
    comm = 0
    
    def __init__(self,port):
        self.comm = serial.Serial(port,9600,timeout=0)
        
    def readNTC(self):
        time.sleep(4)
        s = self.comm.read(10000)
        
        
        for i in range(1,len(s)-2):
            
            if s[len(s)-2-i] == '\n':
                x = int(len(s)-i-2)
                
                #print x    
                a =  s[(x+1):-2]
                
                break
            else:
                if len(s) < 10:
                   
                    a =  s[:-2]
                    break
        return float(a)
            
             
            
            
        
        
        
        #return float(s[x+1:len(s)-2])  
            
            
            
                

    def close(self):
        self.comm.close()

    def open(self):
        self.comm.open()
    
    def s(self):
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
         print self.readNTC()
         
