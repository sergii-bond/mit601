import lib601.poly as poly
import swLab04SignalDefinitions
reload(swLab04SignalDefinitions) # so changes you make in swLab04SignalDefinitions.py will be reloaded
from swLab04SignalDefinitions import *

print StepSignal().samplesInRange(-3, 10)

step1 = ScaledSignal(R(StepSignal()), 3)
step2 = ScaledSignal(Rn(StepSignal(), 7), -3)
stepUpDown = SummedSignal(step1, step2) 
stepUpDownPoly = polyR(UnitSampleSignal(), poly.Polynomial([5, 0, 3, 0, 1, 0]))

print step1.samplesInRange(-3, 10)
print step2.samplesInRange(-3, 10)
print stepUpDown.samplesInRange(-3, 10)
print stepUpDownPoly.samplesInRange(-3, 10)
