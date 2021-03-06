import os
labPath = os.getcwd()
from sys import path
if labPath not in path:
    path.append(labPath)
print 'setting labPath to', labPath

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Remember to change the import in dynamicMoveToPointSkeleton in order
# to use it from inside soar
import dynamicMoveToPointSkeleton
reload(dynamicMoveToPointSkeleton)

import ffSkeleton
reload(ffSkeleton)

from secretMessage import secret
#import secretMessage 
#reload(secretMessage)

# Set to True for verbose output on every step
verbose = False

# Rotated square points
squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]


def cond(inp):
    sensors = inp[1]
    for s in sensors.sonars:
        if s < 0.3:
            return False
    return True

# Put your answer to step 1 here
mySM = sm.Cascade(sm.Parallel(ffSkeleton.FollowFigure(secret), sm.Wire()),
                    sm.Switch(cond, dynamicMoveToPointSkeleton.DynamicMoveToPoint(),
										sm.Constant(io.Action())))

######################################################################
###
###          Brain methods
###
######################################################################


def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail = True)
    robot.behavior = mySM


def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(),
                         verbose = verbose)


def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())


def brainStop():
    pass


def shutdown():
    pass
