import Vibration
import time

test = Vibration.VibrationCycling('COM2','COM10',grmsPort='COM4')
test.cycle(5,10,5, frequency=2)

