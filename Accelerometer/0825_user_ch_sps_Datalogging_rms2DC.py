import pyqtgraph as pg
import time, threading, sys, os,fnmatch, shutil
import serial
import numpy as np
import glob
import pyqtgraph.exporters

"""
[README]
0. Let A0~A5 pins be grounded when not used
1. Before running this, unplug the usb and reconnect it.
"""


"""
Hyoyeon Lee 
Created 2016.08.03
Revised 2016.08.25

[Reference] http://forum.arduino.cc/index.php?topic=137635.15;wap2

[Hardware ] arduino_DUE(loaded with "accDue_user_ch_sps.ino")
	    accelerometer_ADXL001-500g with Power=3.3V (no low-pass filter :C2=22[nF],R1=0[Ohm])
	    rms2dc IC_AD8436B with Power=+-5[V] with switches...
			CORE_BUF(core),INCOUP(AC),IBUF_VCC(dis),OBUF_VCC(en),DC_OUT(core)

[Summary  ] Find a connected Serial '/dev/ttyA*'(arduinoDUE-USB port(Not a programming port!!)
            Read data(16bits) every T[s]
            	 >>>upper( 4 bits) : channelID ( ID2~ID7 corresponds to A5~A0)
		 >>>lower(12 bits) : data with conversion rate 3.3[V]/4095[digits] 
	    Convert to [g] by dividing scaling = 2.2E-3[V/g]*4095[digits]/3.2922[V]
	    Plot data,grms,and zoomed-in 
"""	       


#____________________Find a port connected to Arduino________________________#
print '		Connect the Arduino (USB port)Cable to PC.'
print '		If already connected, UNPLUG and then Reconnect it.'

a = raw_input( '[User] press any key if you connect the port ')
if a is not None:
	print 'Finding the address of the port'
ACMport  = glob.glob('/dev/ttyA*')
for item in ACMport:
	try:    due = serial.Serial(item)
	except: print ''
print 'The Arduino is Connected :'
print '       >>> %s' %due
print ''

#[USER]_______________________user_ch_sps_dt
"""
while True:
	sps=input('[User]Sampling rate of DUE (50 or 100[kHz])	: ')
	if sps not in [50,100]:
		print 'Not 50 or 100 [kHz]'
	else:
		break
"""
sps=50
user_ch_sps_dt =[[6,20E-6],[7,10E-6]]
ch = user_ch_sps_dt[sps/50-1][0]
dt = user_ch_sps_dt[sps/50-1][1]

#print 'Sampling Rate = %d [kHz], dt = %f [sec]' %(sps,dt)


 
#[USER]_______________________plot_type
print ''
"""
plot_rms = input( '[User] RMS Plot (1(y)/0(n))	: ')
if sps==50:
	plot_lr  = input( '[User] ZoomIn Plot (1(y)/0(n))	: ')
else:
	print 'ZoomIn plot is not recommended for sps=%d [kHz]' %sps 
	plot_lr  = input( 'still need to plot ZoomIn?   1(y)/0(n) : ')
ymax     = input('[User] Plot Range (Y max [g])	: ')
#t_range  = input('[User] Plot Range in [sec] (1~5[sec])	: ')
#T        = input('Sampling Time (T) with T <= 1[sec]) :  ')
#nCH      = input('Number of Accelerometers connected to Arduino (1~6) :  ')
"""
plot_rms=0
plot_lr=0
ymax=10
T      = 1
nCH    = 6
t_range= 1
case=(plot_lr<<1)+plot_rms      # case 0-none/ 1-rms/ 2-lr/ 3-rms&lr 
ndump = int((0.1*1E6)/(dt*1E6)) # dump first 0.1[s] data
M     = int((T*1E6)/(dt*1E6))	# each reading       
n     = int(t_range/T)		# plot range 
N     = int(50*n)			# buffer length
scaling  = 2.7365 		# [digits/g] for ADXL001-500z with Power=3.3V

#[USER]_______________________DataLogging
print ''
DataLogging = input( '[User] DataLogging (1(y)/0(n))	 : ')
if DataLogging ==1:
	t_logging   = input( '[User] Logging Period[s]	 : ')
	DataInfo    = raw_input('[User] Key info (pasco/hammer/test)	: ')

#_________________________Threading_______________________________________#
class SerialReader(threading.Thread):
#_________________________________________________________________#	
	def __init__(self, port, M, N):
        	threading.Thread.__init__(self)
        	self.buffer    = np.zeros((N*M,nCH/2),dtype=np.float)
        	#self.buff_digit= np.zeros((N*M,nCH/2),dtype=np.uint16)
		self.buff_rms  = np.zeros((N*M,nCH/2),dtype=np.float)
		self.N         = N                         
        	self.M         = M                         
        	self.ptr       = 0                         
		self.port      = port                      
        	self.sp        = 0.0                       
        	self.exitFlag  = False
        	self.exitMutex = threading.Lock()
        	self.dataMutex = threading.Lock()
#_________________________________________________________________#	
    	def run(self):
        	exitMutex      = self.exitMutex
        	dataMutex      = self.dataMutex
        	buffer         = self.buffer
		#buff_digit     = self.buff_digit
		buff_rms       = self.buff_rms
        	port           = self.port
        	count          = 0
        	sp             = None
        	t1             = pg.ptime.time()
        	while True:
			with exitMutex:                    
        	        	if self.exitFlag:
        	            		break
			mod4   = np.empty((M, ch),dtype=np.uint16)
			rawdata= np.empty((M,nCH),dtype=np.uint16)

        	    	port.flush()
			dump   = port.read(ndump*2*ch)			#dump incorrect reading    
			org    = port.read(self.M*2*ch)			#read data from Due    
        	    	mod1   = np.fromstring(org,dtype=np.uint16)     #convert string to integer
			leading= mod1[0]>>12			        #check the channel ID of the first data
			leading= leading-100/sps
			mod2   = mod1&4095				#remove channel ID and get only acceleration values
			mod3   = mod2.reshape(self.M,ch)		
			for i in range (0,ch):				# column index =  channelID-2 (ch2~ch7)
				mod4[:,(leading+i)%ch] = mod3[:,i]	
			for i in range (0,nCH):				# column index =  pin number  ( A0~ A5)
				rawdata[:,i]=mod4[:,ch-1-i]		# ONLY store data of enabled pins
			mean   = [np.average(rawdata[:,i])          for i in range(0,nCH)]	#mean=mean of rawdata for T
			scaled = [(rawdata[:,i]-mean[i])/scaling    for i in range(0,nCH,2)]	#scaled=converted into [g]
			rms    = [rawdata[:,i]/scaling              for i in range(1,nCH,2)]	#rms=grms
			count += self.M                    
        	    	t2     = pg.ptime.time()
        	    	difft     = t2-t1
        	    	if difft > 1.0:
        	    	    if sp is None:                
        	    	        sp = count / difft
        	    	    else:
        	    	        sp = sp * 0.9 + (count / difft) * 0.1
        	    	    count = 0
        	    	    t1    = t2
        	    	with dataMutex:                    
        	    	    buffer    [ self.ptr : self.ptr+self.M ] = np.transpose(scaled)
			    #buff_digit[ self.ptr : self.ptr+self.M ] = rawdata
			    buff_rms  [self.ptr  : self.ptr+self.M ] = np.transpose(rms)
        	    	    self.ptr = (self.ptr + self.M) % (N*M)
        	    	    if sp is not None:
        	    	        self.sp = sp
#_________________________________________________________________#	

	def get(self, M,n):
       		with self.dataMutex:
			num = M*n                    
        		ptr = self.ptr
			if ptr-num < 0:
        	        	data   = np.empty((num,nCH/2),dtype=np.float)
        	        	data [       :num-ptr] = self.buffer    [ptr-num:   ]
        	        	data [num-ptr:       ] = self.buffer    [       :ptr]
        	        	grms  = np.empty((num,nCH/2),dtype=np.float)
				grms [       :num-ptr] = self.buff_rms[ptr-num:   ]
        	        	grms [num-ptr:       ] = self.buff_rms[       :ptr]
        	    	else:
				data  = self.buffer      [self.ptr-num :self.ptr  ].copy()
				grms  = self.buff_rms    [self.ptr-num :self.ptr  ].copy()
			"""
			if (ptr/M-10*n)<0:
				grms   = np.empty((10*n,nCH),dtype=np.float)
				grms [       :10*n-ptr/M] = self.buff_rms  [ptr/M-10*n:     ]
				grms [10*n-ptr/M:       ] = self.buff_rms  [       :ptr/M]
			else:
				grms  = self.buff_rms    [self.ptr/M-10*n :self.ptr/M].copy()
        	    	"""
			rate = self.sp
        		return data,grms
#_________________________________________________________________#	
	def exit(self):
    		with self.exitMutex:                   
    	        	self.exitFlag = True
##################################################################


app     = pg.mkQApp()        
win	= pg.GraphicsWindow(title=' ************ SAMPLING RATE = %d [kHz]*************'%sps)     
win.resize(1000,400)
lr=pg.LinearRegionItem([0.01,0.05])
lr.setZValue(-10)
#_______________plot1____________________________________
plt1	= win.addPlot(title="ADXL001-500z")
plt1.setLabels(left=('Acceleration','g'),bottom=('Time','s'))
plt1.setYRange(-ymax,ymax)
plt1.setXRange(0 ,t_range)
plt1.showGrid(x=True,y=True)
plt1.addLegend()
accX = plt1.plot(pen=(255,  0,  0),name='A0_accX') #the same color of the wire 
rmsX = plt1.plot(pen=(255,255,  0),name='A1_rmsX')
accY = plt1.plot(pen=(  0,255,  0),name='A2_accY')
rmsY = plt1.plot(pen=(  0,  0,255),name='AD_rmsY')
accZ = plt1.plot(pen=(165, 42, 42),name='A4_accZ')
rmsZ = plt1.plot(pen=(128,  0,128),name='AD_rmsZ')
if DataLogging ==1:
	exporter=pg.exporters.CSVExporter(plt1)


if case==2  or case==3:
	#Linear Region slowers the data aquisition.
	#If needed, activate this with the last def UpdatePlot, etc.
	#_______________plot2____________________________________

	plt1.addItem(lr)
	plt2=win.addPlot(title='Linear Region')
	plt2.setYRange(-ymax,ymax)
	rx=plt2.plot(pen=(255,  0,  0))
	ry=plt2.plot(pen=(  0,255,  0))
	rz=plt2.plot(pen=(165, 42, 42))
	
	def updatePlot():
        	plt2.setXRange(*lr.getRegion(),padding=0)
	def updateRegion():
        	lr.setRegion(plt2.getViewBox().viewRange()[0])

t_data = [i*dt for i in range(0,n*M) ]
#Start Program
thread = SerialReader(due,M,N)
thread.start()
#___________________________________________________________________#
def update():                
	global due,thread,lr
	global plt1,  accX, rmsX, accY, rmsY, accZ, rmsZ
	global plt2,  rx,ry,rz
	
	data,grms = thread.get(M,n)
	

	accX.setData(t_data,data[:,0])
	rmsX.setData(t_data,grms[:,0])
	"""
	accY.setData(t_data,data[:,1])
	rmsY.setData(t_data,grms[:,1])
	accZ.setData(t_data,data[:,2])
	rmsZ.setData(t_data,grms[:,2])
	"""
	
	if case==2 or case==3:
		rx.setData(t_data,data[:,0])
		"""
		ry.setData(t_data,data[:,1])
		rz.setData(t_data,data[:,2])
		"""
	
	if DataLogging==1:
		timestamp=time.time()
		now=int(round(timestamp))
		if (now%t_logging)==0:
			localDATE=time.strftime('%y%m%d'  ,time.localtime(timestamp))
			localTIME=time.strftime('%H:%M:%S',time.localtime(timestamp))
			filename='accData_'+localDATE+'_%s_'%DataInfo + localTIME+'.csv'
			exporter.export(filename)
	if not plt1.isVisible():
		thread.exit()
	        timer.stop()
		due.close()
		due.delete()
#___________________________________________________________________#
timer = pg.QtCore.QTimer()                    
timer.timeout.connect(update)


#___________________________________________________________________#


if case==2 or case==3:

	lr.sigRegionChanged.connect(updatePlot)
	plt2.sigXRangeChanged.connect(updateRegion)
	updatePlot()

timer.start(0)
if sys.flags.interactive == 0:                  
    app.exec_()
