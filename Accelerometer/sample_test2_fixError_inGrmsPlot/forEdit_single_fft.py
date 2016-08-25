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
	data    = readCSV[:,1]
	grms	= rms(data)
	return t_range,data,grms

#___take localTime
hue=['-r','-y','-g','-b','-chocolate','m']



files=sorted(glob.glob('*csv'))		
N=len(files) 				#number of csv files
t_local=np.array(['        ']*(N*2))	#an array to save time as localTime
t_local=t_local.reshape(N,2)
t_int=np.empty(N,dtype=np.int)		#an array to save time as integer

GRMS    = np.empty(N,dtype=np.float)
DATA 	= []
T_RANGE = []
FOURIER = []
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
		tMax=(11*3600+59*60+59)+1
		INFO_initial=list(files[i].split('.'))[0]
	else:
		if intT>t0:
			t_int[i]=intT-t0
		else:
			t_int[i]=(intT-t0)+tMax
	if i==N-1:
		INFO_final=list(files[i].split('.'))[0]
	#OPEN FILE AND CALCULATE GRMS 
	t_range,data,grms = read_data(files[i])
	GRMS[i]=grms
	DATA.append(data)
	T_RANGE.append(t_range)
	freq,fourier = FFT(data)
	FOURIER.append(fourier*grms)
	FREQ.append(freq)
with PdfPages(INFO_initial+'_RESULTS.pdf') as pdf:
	plt.figure(1)
	plt.plot(t_int,GRMS,'-ro')
	plt.title(INFO_initial+' ~ '+INFO_final)
	plt.xlabel('TIME [s]')
	plt.ylabel('Grms [g]')
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
				plt.figure(2)
				plt.subplot(2,1,1)
				plt.plot(T_RANGE[i],DATA[i],'-k')
				plt.title('Elapse Time=%d[s] Grms=%f[g]'%(t_int[i],GRMS[i]),fontweight='bold')
				plt.suptitle('%s'%files[i])
				plt.xlabel('TIME [s]')
				plt.ylabel('AMPLITUDE [g]')
			
				plt.subplot(2,1,2)
				plt.plot(FREQ[i],abs(FOURIER[i]),'-r')
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
			plt.plot(T_RANGE[idx],DATA[idx],'-k')
			plt.title('Elapse Time=%d[s] Grms=%f[g]'%(t_int[idx],GRMS[idx]),fontweight='bold')
			plt.suptitle('%s'%files[idx])
			plt.xlabel('TIME [s]')
			plt.ylabel('AMPLITUDE [g]')
			
			plt.subplot(2,1,2)
			plt.plot(FREQ[idx],abs(FOURIER[idx]),'-r')
			plt.xlabel('FREQUENCY [Hz]')
			plt.ylabel('|FFT*Grms| [g]')
			
			pdf.savefig()
			plt.close

print "Now Check the current Folder"
			
	
	
	
