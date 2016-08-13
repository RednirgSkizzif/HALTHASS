import grms
from sys import argv

script , input = argv


y = grms.read_data(input,1)
mean = grms.rms(y)
print "grms = ", mean
x = grms.plotf(y,mean)
#grms.Integrate(x,10000,50000)


