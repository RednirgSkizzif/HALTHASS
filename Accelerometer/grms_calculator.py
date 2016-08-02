import math

def grms(readings):
	
	sum_squares=0
	for i in range(0,len(readings)):
		sum_squares = sum_squares+readings[i]*readings[i]
	return math.sqrt(sum_squares/len(readings))
	




