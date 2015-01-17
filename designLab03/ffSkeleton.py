import lib601.sm as sm


class FollowFigure(sm.SM):
    def __init__(self, points):
        self.points = points
        self.last = len(points) - 1
        self.startState = 0

    def getNextValues(self, state, sensors):
        robot_point = sensors.odometry.point()
        if not state == self.last:
            if self.points[state].isNear(robot_point, 0.02):
                state = state + 1
        return (state, self.points[state])
