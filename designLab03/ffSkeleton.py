import lib601.sm as sm


class FollowFigure(sm.SM):
    def __init__(self, points):
        self.points = points
        self.startState = 0

    def getNextValues(self, state, sensors):
        robot_point = sensors.odometry.point()
        if not state == 3:
            if self.points[state].isNear(robot_point, 0.05):
                state = state + 1
        return (state, self.points[state])
