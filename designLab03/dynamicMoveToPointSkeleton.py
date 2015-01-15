import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io


class DynamicMoveToPoint(sm.SM):
    def __init__(self):
        self.startState = [0, util.Point(0, 0)]

    def getNextValues(self, state, inp):
        # Replace this definition
        # print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        assert isinstance(inp, tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0], util.Point), 'inp[0] should be a Point'
        goal_point = inp[0]
        sensors = inp[1]  # io.SensorInput
        position = sensors.odometry  # util.Pose
        point = position.point()  # util.Point
        angle = position.theta
        goal_angle = point.angleTo(goal_point)
        st = state[0]
        p0 = state[1]

        if p0 != goal_point:
            st = 0
            p0 = goal_point

        if st == 0:
            fv = 0
            if not util.nearAngle(angle, goal_angle, 0.01):
                rv = -util.fixAnglePlusMinusPi(util.fixAnglePlusMinusPi(angle)
                                        - util.fixAnglePlusMinusPi(goal_angle))
            else:
                rv = 0
                st = 1
        elif st == 1:
            rv = 0
            if not point.isNear(goal_point, 0.01):
                fv = point.distance(goal_point)
            else:
                fv = 0
                st = 2
        else:
            (fv, rv) = (0, 0)

        return ([st, p0], io.Action(fvel=fv, rvel=rv))
