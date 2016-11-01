

import Vibration
import time

print "START"
test = Vibration.VibrationCycling('COM2','COM10')
test.setPressure(20)

test.changeFreq(10)