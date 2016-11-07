import numpy as np
import serial,glob,math
import time,threading,sys,os,fnmatch,shutil
#filename=raw_input("filename:  ")
#import pyqtgraph as pg
#import pyqtgraph.exporters

t_log = 10
filename = "gfile.txt"

t_start = time.time()
localDATE = time.strftime('%y%m%d'  ,time.localtime(t_start))
localTIME = time.strftime('%H:%M:%S',time.localtime(t_start))
fgrmsName = localDATE+'_grms_'+'start_at_'+ localTIME+'.csv'

def facc_Write(y,t):
	localDATE = time.strftime('%y%m%d'  ,time.localtime(t))
	localTIME = time.strftime('%H:%M:%S',time.localtime(t))
	faccName = localDATE+'_acc_'+localTIME+'.csv'
	facc = open(faccName,'w')
	for i in range(0,len(y)):
		facc.write(str(0.0002*i)+' '+str(y[i])[1:-1]+' \n')
	facc.close()


def fgrms_Write(fgrmsName,y,ycomp,t0,t):
	str_t  = str(int(t-t0))
	str_g  = str(y)
	fgrms = open(fgrmsName,'a')
        fgrms.write(str_t+' '+str_g+' ');fgrms.write(str(ycomp)[1:-1]+' \n');fgrms.close()



def fWrite(filename,y):
	try :f = open(filename, 'w');f.flush();f.write(y+'\n');f.close()
	except:print ''
	

def rms(y):
        sum_squares = 0
        for i in range(0,len(y)):
                sum_squares = sum_squares+y[i]*y[i]
        return math.sqrt(sum_squares/float(len(y)))

def findArduino(boardName,exclude):
	a = raw_input('Connect %s and press Enter'%boardName)
	if a is not None:
        	ACMport  = glob.glob('/dev/ttyA*')
        	for i in range(0,len(ACMport)):
                	if ACMport[i]==exclude:	ACMport[i]=0
                	try   :	info=serial.Serial(ACMport[i]);address=ACMport[i]
	                except: print ''
	print '%s = %s'%(boardName,address);print info
	return info,address


sps      = 50
dt       = 0.00002 
ymax     = 600
t_logging= 10
t_avg    = 1.0
M        = int(round(t_avg/dt))	           
N        = 50			   
ch       = 6
toG      = 2.7365 		  
t_data   = [i*dt for i in range(0,M) ]
buffer    	= np.zeros((N*M,ch),dtype=np.float)
buff_rms  	= np.zeros((  M,ch),dtype=np.float)
buff_gt  	= np.zeros((  M   ),dtype=np.float)
class SerialReader(threading.Thread):
	def __init__(self, portR, M, N, ch, toG):
        	threading.Thread.__init__(self)
		self.portR 	= portR         
        	self.M     	= M           
		self.N     	= N                         
		self.ch    	= ch 
		self.t_now=time.time()
		self.toG   	= toG                       
        	self.ptr   	= 0             
		self.sp    	= 0.0                       
        	self.exitFlag  	= False
        	self.exitMutex 	= threading.Lock()
        	self.dataMutex 	= threading.Lock()
    	def run(self):
        	exitMutex      	= self.exitMutex
        	dataMutex      	= self.dataMutex
        	t1             	= time.time()
        	portR      	= self.portR         
        	M	   	= self.M    
		N	       	= self.N
		ch	   	= self.ch
		toG       	= self.toG
		count      	= 0	
		sp        	= None
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:break
			#Read gAMP from DUE
			temp   	= np.empty((M,ch),dtype=np.uint16)
        	    	portR.flush()
			portR.read(int(0.1*M*2*ch))	    
			R      	= portR.read(M*2*ch)
			R      	= np.fromstring(R,dtype=np.uint16) 
			leading	= R[0]>>12           
			leading	= leading-100/sps
			R      	= R&4095	            
			R      	= R.reshape(M,ch)		
			for i in range (0,ch) : temp[:,(leading+i)%ch] =    R[:,     i]	
			for i in range (0,ch) : R[:,i]                 = temp[:,ch-1-i]		
			avg  	= np.array([np.average(R[:,i])  for i in range(0,ch)]) 
			gAMP 	= np.array([(R[:,i]-avg[i])/toG for i in range(0,ch)]).reshape(M,ch)
			gRMS 	= np.array([rms(gAMP[:,i])      for i in range(0,ch)])
			gt 	= np.sqrt(gRMS[0]**2+gRMS[1]**2+gRMS[2]**2)
			self.t_now=time.time()
			print str(gt)
			fWrite(filename,str(gt))
			fgrms_Write(fgrmsName,gt,gRMS,t_start,self.t_now)
			#if count%(M*10)==0:
			#	print "csv out"
			#	facc_Write(gAMP,t_now)
			count  += self.M
			t2	= time.time()
			difft 	= t2-t1
        	    	if difft > 1.0:
				if sp is None : sp = count / difft
        	    		else          : sp = sp * 0.9 + (count / difft) * 0.1
				t1 = t2
        	    	with dataMutex:                    
        	    		buffer  [ self.ptr : self.ptr + M ] = gAMP
        	    		buff_rms[          (self.ptr/M)%N ] = gRMS
				buff_gt [          (self.ptr/M)%N ] = gt
				self.ptr = (self.ptr + self.M) % (N*M)
        	    		if sp is not None : self.sp = sp
	def get(self):
       		with self.dataMutex:
        		ptr = self.ptr
			#M   = self.M
			if ptr==0 : data = buffer[ptr-M :   ]
        	    	else      : data = buffer[ptr-M :ptr].copy()
			rate = self.sp
        		return data 
	def exit(self):
    		with self.exitMutex : self.exitFlag = True

########################################################################################

class Csvfiles(threading.Thread):
	def __init__(self,mainTH):
		self.mainTH=mainTH
        	threading.Thread.__init__(self)
		self.count	= mainTH.ptr  
		self.t_now=mainTH.t_now 
	def run(self):
		mainTH=self.mainTH
        	while True:
			count=mainTH.ptr
			print "                                                    thread2 %d"%(self.count%M)
			if self.count%(M*10)==0:
				print "csv out"
				if self.count==0 : data = buffer[self.count-M :   ]
                        	else          : data = buffer[self.count-M :self.count].copy()
				facc_Write(data,self.t_now)


ArduinoRead = serial.Serial('COM12',9600)
#ArduinoRead, address_read=findArduino('Arduino_read','0')
thread = SerialReader(ArduinoRead,M,N,ch,toG)
thread.start()
thread2 = Csvfiles(thread)
thread2.start()
#######################################################################################
