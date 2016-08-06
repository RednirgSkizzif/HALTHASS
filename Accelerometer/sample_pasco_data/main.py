import grms
from sys import argv

script , input = argv


y = grms.read_data(input,1)
mean = grms.grms(y)
print "grms = ", mean
x = grms.plotf(y,mean)


