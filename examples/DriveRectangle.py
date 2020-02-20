#!/usr/bin/env python3

# imports
#------------
# import log function
from ev3devlogging import timedlog as log
# import ev3 API
from ev3dev2 import auto as ev3

# initialize
#------------
# initialize left and right motor as tank combo
tankDrive = ev3.MoveTank(ev3.OUTPUT_A, ev3.OUTPUT_D)

# initialize some constants
SPEED_FORWARD = ev3.SpeedPercent(30)     # set speed to 30% of maximum speed
SPEED_BACKWARD = ev3.SpeedPercent(-30)   # backward with same speed as forward
SPEED_ZERO   = ev3.SpeedPercent(0)       # stop motor (speed is zero)

TURN_TIME=0.62

# main loop
#-----------
log("drive forward")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_FORWARD, 2)

log("turn right")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_BACKWARD,TURN_TIME)

log("drive forward")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_FORWARD, 3)

log("turn right")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_BACKWARD, TURN_TIME)

log("drive forward")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_FORWARD, 2)

log("turn right")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_BACKWARD, TURN_TIME)

x=1/0

log("drive forward")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_FORWARD, 3)

log("turn right")
tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_BACKWARD, TURN_TIME)

log("finished")

        
