<<<<<<< HEAD




        




import Vibration
import time

test = Vibration.VibrationTest('COM2',5,1,5,'COM11',9600,grmsPort='COM4')
step_size = test.step_size
step_length  =test.step_length
number_of_steps = test.number_of_steps



pressure = 1



for n in range(1,number_of_steps):
        t_end = time.time() + 60 * n * step_length
        while time.time() < t_end:
                x = test.checkGrms()
                print x
                print 'd1'
                if((x < (n*step_size - 1)) and (x > (n*step_size-3))):
                        print 'd2'
                        pressure = pressure + 1
                        if pressure > 50:
                                pressure = 50
                        test.setPressure(pressure)
                elif((x > (n*step_size+1))  and (x < (n*step_size+3))):
                        print 'd3'
                        pressure = pressure - 1
                        if pressure < 1:
                                pressure=1 
                        test.setPressure(pressure)
                elif(x > (n*step_size +3)):
                        print 'd4'
                        pressure = pressure - 3
                        if pressure < 1:
                                pressure=1  
                        test.setPressure(pressure)
                elif(x < n*step_size-3):
                        print 'd5'
                        pressure = pressure + 3
                        if pressure > 50:
                                pressure = 50
                        test.setPressure(pressure)
                                
                x = test.checkGrms()
                while ((x >= (n * step_size - 1)) and (x <= (n * step_size + 1))):
                        print 'd6'
                        time.sleep(1)
                        x = test.checkGrms()
                        print x
                        if time.time() >= t_end:
                                break
        
        
                
