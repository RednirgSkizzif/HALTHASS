

import Vibration
import time

test = Vibration.VibrationTest('COM2',10,5,5,'COM10',9600,grmsPort='COM4')


<<<<<<< HEAD:AirRegulation/RegulatorCycling.py
for n in range(1,number_of_steps):
=======
for n in range(1,number_of_steps)
>>>>>>> d2217de1ab4edbf8ec462f2819b3dd1882b3959d:AirRegulation/RegluatorCycling.py
	
	t_end = time.time() + 60 * n * step_length
	while time.time() < t_end:

		

		test.checkGrms() = grms
		print grms
		if(grms < (n*step_size - 1) and grms > (n*step_size-3)):
			pressure = pressure + 1
			test.setPressure(pressure)
<<<<<<< HEAD:AirRegulation/RegulatorCycling.py
		elif(grms > (n*step_size+1)  and grms < (n*step_size+3)):
=======
		elif(grms > (n*step_size+1) && grms < (n*step_size+3)):
>>>>>>> d2217de1ab4edbf8ec462f2819b3dd1882b3959d:AirRegulation/RegluatorCycling.py
			pressure = pressure - 1
			test.setPressure(pressure)
		elif(grms > (n*step_size +3)):
			pressure = pressure - 3
			test.setPressure(pressure)
<<<<<<< HEAD:AirRegulation/RegulatorCycling.py
		elif(grms < n*step_size-3):
=======
		elif(grms < n*step_size-3)):
>>>>>>> d2217de1ab4edbf8ec462f2819b3dd1882b3959d:AirRegulation/RegluatorCycling.py
			pressure = pressure + 3
			test.setPressure(pressure)
				
		test.checkGrms = grms
		while (grms >= (n * step_size - 1)) and (grms <= (n * step_size + 1)):
			time.sleep(5)
			test.checkGrms = grms
			print grms
			if time.time() >= t_end:
				break
	
		
		


	



