
import lib601.sm as sm
# import lib601.util as util
import operator


class Delay(sm.SM):
    def __init__(self, v0):
        self.startState = v0

    def getNextValues(self, state, inp):
        return (inp, state)


class Increment(sm.SM):
    startState = 0

    def __init__(self, incr):
        self.incr = incr

    def getNextValues(self, state, inp):
        return (state, inp + self.incr)


class Cascade(sm.SM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = [sm1.startState, sm2.startState]

    def getNextValues(self, state, inp):
        (state1, out1) = self.sm1.getNextValues(state[0], inp)
        (state2, out) = self.sm2.getNextValues(state[1], out1)
        return ([state1, state2], out)


class Parallel(sm.SM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = [sm1.startState, sm2.startState]

    def getNextValues(self, state, inp):
        (state1, out1) = self.sm1.getNextValues(state[0], inp)
        (state2, out2) = self.sm2.getNextValues(state[1], inp)
        return ([state1, state2], [out1, out2])


class PureFunction(sm.SM):
    def __init__(self, f):
        self.f = f
        self.startState = 0

    def getNextValues(self, state, inp):
        return (state, self.f(inp))

sm1 = Delay(1)
sm2 = Delay(2)
c = sm.Cascade(sm1, sm2)
d = Cascade(sm1, sm2)
print c.transduce([3, 5, 7, 9])
print d.transduce([3, 5, 7, 9])

sm1 = Delay(1)
sm2 = Increment(3)
c = sm.Cascade(sm1, sm2)
d = Cascade(sm1, sm2)
print c.transduce([3, 5, 7, 9])
print d.transduce([3, 5, 7, 9])


def f1(inp):
    return inp * 2

sm1 = PureFunction(f1)
print sm1.transduce([3, 5, 7, 9])


class BA1(sm.SM):
    startState = 0

    def getNextValues(self, state, inp):
        if inp != 0:
            newState = state * 1.02 + inp - 100
        else:
            newState = state * 1.02
        return (newState, newState)


class BA2(sm.SM):
    startState = 0

    def getNextValues(self, state, inp):
        newState = state * 1.01 + inp
        return (newState, newState)


class MaxAccount(sm.SM):

    def __init__(self):
        self.startState = [0, 0]
        self.p = sm.Parallel(BA1(), BA2())
        self.pf = sm.PureFunction(max)

    def getNextValues(self, state, inp):
        (pstate, pout) = self.p.getNextValues(state, inp)
        (pfstate, pfout) = self.pf.getNextValues(0, pout)
        return (pstate, pfout)


class SwitchAccount(sm.SM):

    def __init__(self):
        self.startState = [0, 0]
        self.p = sm.Parallel2(BA1(), BA2())
        self.pf = sm.PureFunction(sum)

    def getNextValues(self, state, inp):
        (pstate, pout) = self.p.getNextValues(state, inp)
        (pfstate, pfout) = self.pf.getNextValues(0, pout)
        return (pstate, pfout)

p = MaxAccount()
print p.transduce([100, 10, -10, 5, -5])
c = SwitchAccount()
print c.transduce([(3001, 0), (0, 10), (-4000, 0), (0, 50), (0, -5)])


class SumTSM(sm.SM):
    def __init__(self):
        self.startState = [0, 0]

    def done(self, state):
        return state[0] == 1

    def getNextValues(self, state, inp):
        if state[0] == 0:
            next_out = state[1] + inp
            if next_out > 100:
                out = inp
                next_state = 1
            else:
                out = next_out
                next_state = 0
        else:
            next_state = 1
            out = state[1]

        return ([next_state, out], out)


s = SumTSM()
print s.transduce([1, 2, 3, 8, 10, 50, 30, 35, 12, 15, 19, 34])


class CountUpTo(sm.SM):
    def __init__(self, v_stop):
        self.startState = 0
        self.stop_val = v_stop

    def done(self, state):
        return state == self.stop_val

    def getNextValues(self, state, inp):
        out = state + 1
        return (out, out)

c = CountUpTo(30)
print c.run(n=20)


def makeSequenceCounter(nums):
    return [CountUpTo(x).run() for x in nums]

print makeSequenceCounter([2, 3, 5])

negate = PureFunction(operator.not_)
c = sm.Feedback(sm.Cascade(negate, Delay(True)))

print c.run(n=10)
