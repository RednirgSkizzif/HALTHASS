import numpy as np
import sys,os,glob
import math
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import fft as fft_scipy



#[FUNCTION]rms
def rms(y):
	sum_squares = 0
	for i in range(0,len(y)):
		sum_squares = sum_squares+y[i]*y[i]
	return math.sqrt(sum_squares/float(len(y)))

#[FUNCTION]fft
def FFT(y):
	n=len(y)
	k=np.arange(n)
	frq=k/1.0	
	freq=frq[range(n/2)]	#frequency
	Y=np.fft.fft(y)/n
	Y=Y[range(n/2)]
	
	sum=0
	for i in range(0,len(Y)):
		sum=sum+abs(Y[i])
	Y=Y*(1/sum) 
	return freq,Y		#renormalized FFT

#[FUNCTION]find index
def find_nearest(array,value):
	array=np.array(array)
	idx = np.abs(array-value).argmin()
	return idx



#[FUNCTION]open
def read_data(dataFile):
	readCSV = np.genfromtxt(dataFile,skip_header=1,delimiter=',')
	t_range = readCSV[:,0]
	dataX   = readCSV[:,1]
	grmsX	= readCSV[:,3]
	dataY   = readCSV[:,5]
	grmsY	= readCSV[:,7]
	dataZ   = readCSV[:,9]
	grmsZ	= readCSV[:,11]
	
	#rms_ad  = grms
	rms_adX   = np.mean(grmsX)
	rms_adxlX = rms(dataX)
	rms_adY   = np.mean(grmsY)
	rms_adxlY = rms(dataY)
	rms_adZ   = np.mean(grmsZ)
	rms_adxlZ = rms(dataZ)
	return t_range,dataX,rms_adX,rms_adxlX,dataY,rms_adY,rms_adxlY,dataZ,rms_adZ,rms_adxlZ



#___take localTime
hue=['-r','-y','-g','-b','-chocolate','m']



files=sorted(glob.glob('*csv'))		
files=files[2:len(files)-1]		#first file gives 0 and the last one may not complete form
N=len(files) 				#number of csv files
t_local=np.array(['        ']*(N*2))	#an array to save time as localTime
t_local=t_local.reshape(N,2)
t_int=np.empty(N,dtype=np.int)		#an array to save time as integer

RMS_ADX    = []
RMS_ADXLX  = np.empty(N,dtype=np.float)
DATAX 	= []
FOURIERX = []

RMS_ADY    = []
RMS_ADXLY  = np.empty(N,dtype=np.float)
DATAY 	= []
FOURIERY = []

RMS_ADZ    = []
RMS_ADXLZ  = np.empty(N,dtype=np.float)
DATAZ 	= []
FOURIERZ = []

T_RANGE = []
FREQ	= []
for i in range(0,N):
	#TIME AS LOCAL DATE AND INTEGER
	name=files[i].split('_')
	t_local[i][0]=name[1]
	t_local[i][1]=list(name[len(name)-1].split('.'))[0]
	print 'date %s time %s' %(t_local[i][0],t_local[i][1])
	strT=list(t_local[i][1].split(':'))
	intT=int(strT[0])*3600+int(strT[1])*60+int(strT[2])
	if i==0:
		t0=intT
		t_int[i]=0
		tMax=12*3600
		INFO_initial=list(files[i].split('.'))[0]
	else:
		if intT>t0:
			t_int[i]=intT-t0
		else:
			t_int[i]=(intT-t0)+tMax
	if i==N-1:
		INFO_final=list(files[i].split('.'))[0]
	#OPEN FILE AND CALCULATE GRMS 
	t_range,dataX,rms_adX,rms_adxlX,dataY,rms_adY,rms_adxlY,dataZ,rms_adZ,rms_adxlZ = read_data(files[i])
	RMS_ADX.append(rms_adX)
	RMS_ADXLX[i]= rms_adxlX
	DATAX.append(dataX)
	
	RMS_ADY.append(rms_adY)
	RMS_ADXLY[i]= rms_adxlY
	DATAY.append(dataY)
	
	RMS_ADZ.append(rms_adZ)
	RMS_ADXLZ[i]= rms_adxlZ
	DATAZ.append(dataZ)
	
	T_RANGE.append(t_range)
	
	freq,fourierX = FFT(dataX)
	FOURIERX.append(fourierX*rms_adxlX)
	
	freq,fourierY = FFT(dataY)
	FOURIERY.append(fourierY*rms_adxlY)
	
	freq,fourierZ = FFT(dataZ)
	FOURIERZ.append(fourierZ*rms_adxlZ)
	FREQ.append(freq)


with PdfPages('RESULT_'+INFO_initial+'.pdf') as pdf:
	fig,ax1=plt.subplots()
	plt.ylabel('GRMS [g]')
	plt.xlabel('Elapse Time [s]')
	ax1.plot(t_int,RMS_ADX,':rx')
	ax1.plot(t_int,RMS_ADY,':gx')
	ax1.plot(t_int,RMS_ADZ,':bx')
	box = ax1.get_position()
	ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	ax1.legend(['ICx','ICy','ICz'],loc='center left', bbox_to_anchor=(1.1, 0.5))
	#ax1.title(INFO_initial+' ~ '+INFO_final)
	#ax1.xlabel('TIME [s]')
	#ax1.ylabel('Grms [g]')
	for tl in ax1.get_yticklabels():
		tl.set_color('y')
	ax2=ax1.twinx()
	ax2.plot(t_int,RMS_ADXLX,'-ro')
	ax2.plot(t_int,RMS_ADXLY,'-go')
	ax2.plot(t_int,RMS_ADXLZ,'-bo')
	box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax2.legend(['ACCx','ACCy','ACCz'],loc='upper left', bbox_to_anchor=(1.1, 0.8))
	#ax2.ylabel('rms to dc IC',color='r')
	for tl in ax2.get_yticklabels():
		tl.set_color('r')
	pdf.savefig()
	print "Grms Plot is coming...(also saved as a pdf)."
	plt.show()
	print " Data and FFT plots? "
	print "          --------------------------------------- "
	print "		 (0)	No Plots         "
	print "		 (1)	For all times    "
	print "	 	 (2)    Selected times   "
	print "          --------------------------------------- "
	sub=input("[User] (0, 1, or 2) : ")
	plt.close
	
	if sub==1:
		allPlots= input("[User] Individual Plots for all times?(y(1)/n(0)): ")
		if allPlots==1:
			for i in range(0,N):
				plt.figure(1)
				plt.subplot(2,1,1)
				plt.plot(T_RANGE[i],DATAX[i],'-r')
				plt.plot(T_RANGE[i],DATAY[i],'-g')
				plt.plot(T_RANGE[i],DATAZ[i],'-b')
				plt.title('Elapse Time=%d[s] Grms=(%0.2f,%0.2f,%0.2f)[g]'%(t_int[idx],RMS_ADXLX[idx],RMS_ADXLY[idx],RMS_ADXLZ[idx]),fontweight='bold')
				plt.suptitle('%s'%files[i])
				plt.xlabel('TIME [s]')
				plt.ylabel('AMPLITUDE [g]')
			
				plt.subplot(2,1,2)
				plt.plot(FREQ[i],abs(FOURIERX[i]),'-r')
				plt.plot(FREQ[i],abs(FOURIERY[i]),'-g')
				plt.plot(FREQ[i],abs(FOURIERZ[i]),'-b')
				plt.xlabel('FREQUENCY [Hz]')
				plt.ylabel('|FFT*Grms| [g]')
				pdf.savefig()
				plt.close
			
	if sub==2:
		pick=input("[User] Enter the time[sec] valuse to plot (','): ")
		for i in pick:
			idx=find_nearest(t_int,i)
			plt.figure(2)
			plt.subplot(2,1,1)
			plt.plot(T_RANGE[idx],DATAX[idx],'-r')
			plt.plot(T_RANGE[idx],DATAY[idx],'-g')
			plt.plot(T_RANGE[idx],DATAZ[idx],'-b')
			plt.title('Elapse Time=%d[s] Grms=(%0.2f,%0.2f,%0.2f)[g]'%(t_int[idx],RMS_ADXLX[idx],RMS_ADXLY[idx],RMS_ADXLZ[idx]),fontweight='bold')
			plt.suptitle('%s'%files[idx])
			plt.xlabel('TIME [s]')
			plt.ylabel('AMPLITUDE [g]')
			
			plt.subplot(2,1,2)
			plt.plot(FREQ[idx],abs(FOURIERX[idx]),'-r')
			plt.plot(FREQ[idx],abs(FOURIERY[idx]),'-g')
			plt.plot(FREQ[idx],abs(FOURIERZ[idx]),'-b')
			plt.xlabel('FREQUENCY [Hz]')
			plt.ylabel('|FFT*Grms| [g]')
			
			pdf.savefig()
			plt.close

print "Now Check the current Folder"
			
	
	
	
