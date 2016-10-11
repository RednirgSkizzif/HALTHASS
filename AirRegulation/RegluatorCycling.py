

import Vibration
import time

test = Vibration.VibrationTest('COM2',10,5,5,'COM10',9600,grmsPort='COM4')


for n in range(1,number_of_steps)
	
	t_end = time.time() + 60 * n * step_length
	while time.time() < t_end:

		

		test.checkGrms() = grms
		print grms
		if(grms < (n*step_size - 1) && grms > (n*step_size-3)):
			pressure = pressure + 1
			test.setPressure(pressure)
		elif(grms > (n*step_size+1) && grms < (n*step_size+3)):
			pressure = pressure - 1
			test.setPressure(pressure)
		elif(grms > (n*step_size +3)):
			pressure = pressure - 3
			test.setPressure(pressure)
		elif(grms < n*step_size-3)):
			pressure = pressure + 3
			test.setPressure(pressure)
				
		test.checkGrms = grms
		while (grms >= (n * step_size - 1)) && (grms <= (n * step_size + 1):
			time.sleep(5)
			test.checkGrms = grms
			print grms
			if time.time() >= t_end:
				break
	
		
		


	



