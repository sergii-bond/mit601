import lib601.poly as poly
import lib601.sig
from lib601.sig import *

# You can evaluate expressions that use any of the classes or
# functions from the sig module (Signals class, etc.).  You do not
# need to prefix them with "sig."

# my comment
# c = UnitSampleSignal()
# c = CosineSignal(4, 1.5)
# c.plot(-5, 5)


def samplesInRange(signal, lo, hi):
    return [signal.sample(i) for i in range(lo,hi)] 


step1 = ScaledSignal(Rn(StepSignal(), 3), 3)
step2 = ScaledSignal(Rn(StepSignal(), 7), -3)
stepUpDown = SummedSignal(step1, step2) 
stepUpDownPoly = polyR(UnitSampleSignal(), poly.Polynomial([5, 0, 3, 0, 1, 0]))

print samplesInRange(StepSignal(), -3, 10)
print samplesInRange(step1, -3, 10)
print samplesInRange(step2, -3, 10)
print samplesInRange(stepUpDown, -3, 10)
print samplesInRange(stepUpDownPoly, -3, 10)
