import grms
from sys import argv

script , input = argv


y = grms.read_data(input,1)
mean = grms.rms(y)
print "grms = ", mean
plotname = raw_input("Give name you want to save the plot as (foo.png)")
x = grms.plotf(y,mean,plotname)
#grms.Integrate(x,10000,50000)


