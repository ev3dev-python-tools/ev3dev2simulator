#!/usr/bin/env python3

# imports
#------------
# import log function
from ev3devlogging import timedlog as log
# import ev3 API
from ev3dev2 import auto as ev3

# initialize
#------------
# initialize color sensor 
colorSensor = ev3.ColorSensor(ev3.INPUT_2)
# initialize left and right motor as tank combo
tankDrive = ev3.MoveTank(ev3.OUTPUT_A, ev3.OUTPUT_D)

# initialize some constants
SPEED_FORWARD = ev3.SpeedPercent(30)     # set speed to 30% of maximum speed
SPEED_BACKWARD = ev3.SpeedPercent(-30)   # backward with same speed as forward
SPEED_ZERO   = ev3.SpeedPercent(0)       # stop motor (speed is zero)

# main loop
#-----------
log("drive forward")
tankDrive.on(SPEED_FORWARD, SPEED_FORWARD)
while True:
    color = colorSensor.color
    if color == colorSensor.COLOR_BLACK: # hit black border line
        print("border!")
        log("detect black")
        # immediately stop
        log("stop")
        tankDrive.stop()
        # drive backwards for the duration of 1 second
        log("drive backwards")
        tankDrive.on_for_seconds(SPEED_BACKWARD, SPEED_BACKWARD, 1)
        # rotate right for 1 second by only running the left motor forward (keep right motor off)
        log("turn right")
        tankDrive.on_for_seconds(SPEED_FORWARD, SPEED_ZERO, 1)
        log("drive forward")
        tankDrive.on(SPEED_FORWARD, SPEED_FORWARD)