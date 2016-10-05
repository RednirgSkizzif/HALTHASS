import numpy as np
import sys,os,glob,math
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#Is3D = input("is this measurement of 3D? Y(1)/N(0)")
Is3D=1
set0='Acc-x'
set1=' IC-x'
set2='Acc-y'
set3=' IC-y'
set4='Acc-z'
set5=' IC-z'
#[FUNCTION]plot ACC,IC FFT__________________________________________
def plot_AccIcFft(fileInfo,setInfo,color,T,rms,t,acc,ic,f,fft):
	plt.subplot(2,1,1)      ; plt.suptitle(setInfo+'  %s' %fileInfo)
	plt.plot(t,acc,color)    ; plt.plot(t,ic,'-k')
	plt.title('Elapse Time=%d[s]'%T,loc='center') ; plt.title('Grms=%0.1f[g]'%rms,loc='right')
	plt.xlabel('TIME [s]')                               ; plt.ylabel('AMPLITUDE [g]')
	plt.subplot(2,1,2)                                   ; plt.plot(f,abs(fft),color)
	plt.xlabel('FREQUENCY [Hz]')                         ; plt.ylabel('|FFT|*Grms [g]')
	pdf.savefig()
	plt.close('all')


#[FUNCTION]rms__________________________________________
def rms(y):
	sum_squares = 0
	for i in range(0,len(y)):
		sum_squares = sum_squares+y[i]*y[i]
	return math.sqrt(sum_squares/float(len(y)))

	
#[FUNCTION]fft__________________________________________
def FFT(y):
	n=len(y)
	k=np.arange(n)
	frq=k/1.0	
	freq=frq[range(n/2)]
	Y=np.fft.fft(y)/n
	Y=Y[range(n/2)]
	sum=0
	for i in range(0,len(Y)):
		sum=sum+abs(Y[i])
	Y=Y*(1/sum) 
	return freq,Y	


#[FUNCTION]find index___________________________________
def find_nearest(array,value):
	array=np.array(array)
	idx = np.abs(array-value).argmin()
	return idx


#[FUNCTION]open_________________________________________
def read_data(dataFile):
	readCSV  = np.genfromtxt(dataFile,skip_header=1,delimiter=',')
	t_range  = readCSV[:,0]; 
	acc0 = readCSV[:,1]; ic0 = readCSV[:, 3] ; rms_acc0 = rms(acc0); rms_ic0  = ic0[len(ic0)/2]
	acc1 = readCSV[:,5]; ic1 = readCSV[:, 7] ; rms_acc1 = rms(acc1); rms_ic1  = ic1[len(ic1)/2]
	acc2 = readCSV[:,9]; ic2 = readCSV[:,11] ; rms_acc2 = rms(acc2); rms_ic2  = ic2[len(ic2)/2]
	
	return t_range,acc0,ic0,rms_acc0,rms_ic0,acc1,ic1,rms_acc1,rms_ic1,acc2,ic2,rms_acc2,rms_ic2


#csv-file names.............................................
files = sorted(glob.glob('*csv'))		
files = files[1:len(files)-1]		        #first and the last one may not complete form
N     = len(files) 				
#create arrays----------------------------------------------
t_local   = np.array(['        ']*(N*2))	
t_local   = t_local.reshape(N,2)
t_rms = np.empty(N,dtype=np.int)		
T_RANGE = []
FREQ    = []
ACC0 = []; IC0 = []; RMS_ACC0 = []; RMS_IC0 = []; FOURIER0 = []
ACC1 = []; IC1 = []; RMS_ACC1 = []; RMS_IC1 = []; FOURIER1 = []
ACC2 = []; IC2 = []; RMS_ACC2 = []; RMS_IC2 = []; FOURIER2 = []


#FILL the ARRAYS
for i in range(0,N):
  #____________________________________________________________take localTime as int
	name=files[i].split('_')
	t_local[i][0]=name[1]
	t_local[i][1]=list(name[len(name)-1].split('.'))[0]
	print 'date %s time %s' %(t_local[i][0],t_local[i][1])
	strT=list(t_local[i][1].split(':'))
	intT=int(strT[0])*3600+int(strT[1])*60+int(strT[2])
	if i==0:
		t0=intT
		t_rms[i]=0
		tMax=12*3600
		INFO_initial=list(files[i].split('.'))[0]
	else:
		if intT>t0:
			t_rms[i]=intT-t0
		else:
			t_rms[i]=(intT-t0)+tMax
	if i==N-1:
		INFO_final=list(files[i].split('.'))[0]
  #___________________________________________________________get data 
	t_range,acc0,ic0,rms_acc0,rms_ic0,acc1,ic1,rms_acc1,rms_ic1,acc2,ic2,rms_acc2,rms_ic2 = read_data(files[i])

	T_RANGE.append(t_range)
	ACC0.append(acc0); IC0.append( ic0); RMS_ACC0.append(rms_acc0); RMS_IC0.append(rms_ic0)
	ACC1.append(acc1); IC1.append( ic1); RMS_ACC1.append(rms_acc1);	RMS_IC1.append(rms_ic1)
	ACC2.append(acc2); IC2.append( ic2); RMS_ACC2.append(rms_acc2);	RMS_IC2.append(rms_ic2)
	freq,fourier0 = FFT(acc0); FOURIER0.append(fourier0*rms_acc0)
	freq,fourier1 = FFT(acc1); FOURIER1.append(fourier1*rms_acc1)
	freq,fourier2 = FFT(acc2); FOURIER2.append(fourier2*rms_acc2)
	FREQ.append(freq)
  #___________________________________________________________vector sum if needed 
if Is3D==1:
	RMS_ACC0 =np.array(RMS_ACC0 );RMS_IC0 =np.array(RMS_IC0 )
	RMS_ACC1 =np.array(RMS_ACC1 );RMS_IC1 =np.array(RMS_IC1 )
	RMS_ACC2 =np.array(RMS_ACC2 );RMS_IC2 =np.array(RMS_IC2 )
	VectorSum_ACC = np.sqrt(RMS_ACC0**2 + RMS_ACC1**2 + RMS_ACC2**2)
	VectorSum_IC  = np.sqrt( RMS_IC0**2 +  RMS_IC1**2 +  RMS_IC2**2)
if Is3D==0:
	RMS_ACC0 =np.array(RMS_ACC0);RMS_IC0=np.array(RMS_IC0)
	RMS_ACC1 =np.array(RMS_ACC1);RMS_IC1=np.array(RMS_IC1)
	RMS_ACC2 =np.array(RMS_ACC2);RMS_IC2=np.array(RMS_IC2)

#create plots

with PdfPages('RESULT_'+INFO_initial+'.pdf') as pdf:
	if Is3D==0:
		plt.figure(998,figsize=(8.27,11.69), dpi=100)
		plt.subplot(2,1,1)
		plt.ylabel('CORRELATION');plt.xlabel('Grms on Vac.Chuck [g]')
		plt.plot(RMS_ACC2,RMS_ACC0,':bv');plt.plot(RMS_ACC2,RMS_ACC1,':g^');plt.plot(RMS_ACC2,RMS_IC2,':rx')
		plt.legend([set0,set1,set3],loc='upper left')
		plt.subplot(2,1,2)
		plt.ylabel('Ratio w.r.t Acc on Vac.Chuck');plt.xlabel('Elapse Time [s]')
		plt.plot(t_rms,ratio0,'-bv');plt.plot(t_rms,ratio1,'-g^');plt.plot(t_rms,ratioIC,':rx')
		plt.legend([set0,set1,set3],loc='upper left')
		pdf.savefig()
	plt.figure(999,figsize=(8.27,11.69), dpi=100)
        if Is3D==1:
		plt.subplot(2,1,1)
		plt.ylabel('Vector Sum of GRMS [g]') ;plt.xlabel('Elapse Time [s]')
		plt.plot(t_rms,VectorSum_ACC,  '-ko');plt.plot(t_rms,VectorSum_IC ,  ':kx')
		plt.legend(['Acc','IC'],loc='upper right')
	if Is3D==0:
		plt.subplot(2,1,1)
		plt.ylabel('Deviation from Vac.Chuck');plt.xlabel('[%]')
		n,bins,patches=plt.hist(Hist0,50,normed=1,facecolor='b')
		n,bins,patches=plt.hist(Hist1,50,normed=1,facecolor='g')
		plt.legend([set0,set1],loc='upper left')
	plt.subplot(2,1,2)
	plt.ylabel(       'GRMS [g]')  ; plt.xlabel('Elapse Time [s]')
	plt.plot(t_rms,RMS_ACC0, '-bv'); plt.plot(t_rms, RMS_IC0, ':bv',fillstyle='none')
	plt.plot(t_rms,RMS_ACC1, '-g^'); plt.plot(t_rms, RMS_IC1, ':g^',fillstyle='none')
	plt.plot(t_rms,RMS_ACC2, '-r>'); plt.plot(t_rms, RMS_IC2, ':r>',fillstyle='none')
	plt.legend([set0,set1,set2,set3,set4,set5],loc='upper left')
	pdf.savefig()
	
	print "Grms Plot is coming...(also saved as a pdf)."
	plt.show()
	"""
	print " Data and FFT plots? "
	print "          --------------------------------------- "
	print "		 (0)	No Plots         "
	print "		 (1)	For all times    "
	print "	 	 (2)    Selected times   "
	print "          --------------------------------------- "
	sub=input("[User] (0, 1, or 2) : ")
	"""
	plt.close('all')
	sub=0
	if sub==1:
		allPlots= input("[User] Individual Plots for all times?(y(1)/n(0)): ")
		if allPlots==1:
			for i in range(0,N):
				#fig-set0
				plt.figure(num=i*10,figsize=(8.27,11.69), dpi=100)
				plot_AccIcFft(files[i],set0,'-b',t_rms[i],RMS_ACC0[i],T_RANGE[i],ACC0[i],IC0[i],FREQ[i],FOURIER0[i])
				plt.figure(num=i*10+1,figsize=(8.27,11.69), dpi=100)
				plot_AccIcFft(files[i],set1,'-g',t_rms[i],RMS_ACC1[i],T_RANGE[i],ACC1[i],IC1[i],FREQ[i],FOURIER1[i])
				plt.figure(num=i*10+2,figsize=(8.27,11.69), dpi=100)
				plot_AccIcFft(files[i],set2,'-r',t_rms[i],RMS_ACC2[i],T_RANGE[i],ACC2[i],IC2[i],FREQ[i],FOURIER2[i])
				"""
				plt.subplot(2,1,1)                                   ; plt.suptitle(set0+'  %s' %files[i])
				plt.plot(T_RANGE[i],ACC0[i],'-b')                    ; plt.plot(T_RANGE[i], IC0[i],'-k')
				plt.title('Elapse Time=%d[s]'%t_rms[i],loc='center') ; plt.title('Grms=%0.1f[g]'%RMS_ACC0[i],loc='right')
				plt.xlabel('TIME [s]')                               ; plt.ylabel('AMPLITUDE [g]')
				plt.subplot(2,1,2)                                   ; plt.plot(FREQ[i],abs(FOURIER0[i]),'-b')
				plt.xlabel('FREQUENCY [Hz]')                         ; plt.ylabel('|FFT|*Grms [g]')
				pdf.savefig()
				plt.close('all')
				#fig-set1
				plt.figure(num=i*10+1,figsize=(8.27,11.69), dpi=100)
				plt.subplot(2,1,1)                                   ; plt.suptitle(set1+'  %s' %files[i])
				plt.plot(T_RANGE[i],ACC1[i],'-g')                    ; plt.plot(T_RANGE[i], IC1[i],'-k')
				plt.title('Elapse Time=%d[s]'%t_rms[i],loc='center') ; plt.title('Grms=%0.1f[g]'%RMS_ACC1[i],loc='right')
				plt.xlabel('TIME [s]')                               ; plt.ylabel('AMPLITUDE [g]')
				plt.subplot(2,1,2)                                   ; plt.plot(FREQ[i],abs(FOURIER1[i]),'-g')
				plt.xlabel('FREQUENCY [Hz]')                         ; plt.ylabel('|FFT|*Grms [g]')
				pdf.savefig()
				plt.close('all')
				#fig-set2
				plt.figure(num=i*10+2,figsize=(8.27,11.69), dpi=100)
				plt.subplot(2,1,1)				     ; plt.suptitle(set2+'  %s' %files[i])
				plt.plot(T_RANGE[i],ACC2[i],'-r')                    ; plt.plot(T_RANGE[i], IC2[i],'-k')
				plt.title('Elapse Time=%d[s]'%t_rms[i],loc='center') ; plt.title('Grms=%0.1f[g]'%RMS_ACC2[i],loc='right')
				plt.xlabel('TIME [s]')                               ; plt.ylabel('AMPLITUDE [g]')
				plt.subplot(2,1,2)                                   ; plt.plot(FREQ[i],abs(FOURIER2[i]),'-r')
				plt.xlabel('FREQUENCY [Hz]')                         ; plt.ylabel('|FFT|*Grms [g]')
				pdf.savefig()
				plt.close('all')
                                """
	if sub==2:
		pick=input("[User] Enter the time[sec] valuse to plot (','): ")
		j=0
		for i in pick:
			idx=find_nearest(t_rms,i)
			plt.figure(num=j*10,figsize=(8.27,11.69), dpi=100)
			plot_AccIcFft(files[idx],set0,'-b',t_rms[idx],RMS_ACC0[idx],T_RANGE[idx],ACC0[idx],IC0[idx],FREQ[idx],FOURIER0[idx])
			plt.figure(num=j*10+1,figsize=(8.27,11.69), dpi=100)
			plot_AccIcFft(files[idx],set1,'-g',t_rms[idx],RMS_ACC1[idx],T_RANGE[idx],ACC1[idx],IC1[idx],FREQ[idx],FOURIER1[idx])
			plt.figure(num=j*10+2,figsize=(8.27,11.69), dpi=100)
			plot_AccIcFft(files[idx],set2,'-r',t_rms[idx],RMS_ACC2[idx],T_RANGE[idx],ACC2[idx],IC2[idx],FREQ[idx],FOURIER2[idx])
			"""
			plt.subplot(2,1,1)
			plt.plot(T_RANGE[idx],ACCX[idx],'-b')
			#plt.ylim([-25,25])
			plt.plot(T_RANGE[idx], ICX[idx],'-k')
			#plt.ylim([-25,25])
			plt.title('Elapse Time=%d[s] GrmsX=%0.2f[g]'%(t_rms[idx],RMS_ACCX[idx]),fontweight='bold')
			plt.suptitle('%s'%files[idx])
			plt.subplot(2,1,2)
			plt.plot(FREQ[idx],abs(FOURIERX[idx]),'-b')
			plt.xlabel('FREQUENCY [Hz]')
			plt.ylabel('|FFT|*GrmsX [g]')
			pdf.savefig()
			plt.close('all')

			plt.figure(num=j*10+1,figsize=(8.27,11.69), dpi=100)
			plt.subplot(2,1,1)
			plt.plot(T_RANGE[idx],ACCY[idx],'-g')
			#plt.ylim([-25,25])
			plt.plot(T_RANGE[idx], ICY[idx],'-k')
			#plt.ylim([-25,25])
			plt.title('Elapse Time=%d[s] GrmsY=%0.2f[g]'%(t_rms[idx],RMS_ACCY[idx]),fontweight='bold')
			plt.suptitle('%s'%files[idx])
			
			plt.subplot(2,1,2)
			plt.plot(FREQ[idx],abs(FOURIERY[idx]),'-g')
			plt.xlabel('FREQUENCY [Hz]')
			plt.ylabel('|FFT|*GrmsY [g]')
			pdf.savefig()
			plt.close('all')

			plt.figure(num=j*10+2,figsize=(8.27,11.69), dpi=100)
			plt.subplot(2,1,1)
			plt.plot(T_RANGE[idx],ACCZ[idx],'-r')
			#plt.ylim([-25,25])
			plt.plot(T_RANGE[idx], ICZ[idx],'-k')
			#plt.ylim([-25,25])
			plt.title('Elapse Time=%d[s] GrmsZ=%0.2f[g]'%(t_rms[idx],RMS_ACCZ[idx]),fontweight='bold')
			plt.suptitle('%s'%files[idx])
			
			plt.subplot(2,1,2)
			plt.plot(FREQ[idx],abs(FOURIERZ[idx]),'-r')
			plt.xlabel('FREQUENCY [Hz]')
			plt.ylabel('|FFT|*GrmsZ [g]')
			pdf.savefig()
			plt.close('all')
			"""
			j=j+1
print "Now Check the current Folder"
			
	
	
	
