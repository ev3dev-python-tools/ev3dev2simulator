#!/usr/bin/env python3

from ev3devlogging import timedlog as log

from ev3dev2 import auto as ev3


# initialize
#------------

# initialize sensors 
colorSensor = ev3.ColorSensor(ev3.INPUT_2)
touchSensorLeft = ev3.TouchSensor(ev3.INPUT_1)
touchSensorRight = ev3.TouchSensor(ev3.INPUT_4)

# initialize left and right motor as tank combo
tankDrive = ev3.MoveTank(ev3.OUTPUT_A, ev3.OUTPUT_D)




# define some functions
#-----------------------

def reverseSmallDistance():
    numberOfMotorRotationsBackwards=1
    tankDrive.on_for_rotations(ev3.SpeedPercent(-35), ev3.SpeedPercent(-35), numberOfMotorRotationsBackwards, brake=False)

def rotateDegrees(degrees):
    degrees = degrees * 2
    tankDrive.on_for_degrees(ev3.SpeedPercent(40), ev3.SpeedPercent(0), degrees, brake=False)

def checkCollision():
    return touchSensorLeft.is_pressed or touchSensorRight.is_pressed



# main loop
#-----------



tankDrive.on(ev3.SpeedPercent(30), ev3.SpeedPercent(30))
while True:
    color = colorSensor.color
    if color == colorSensor.COLOR_BLACK: # black line
        log("border")
        tankDrive.stop()
        reverseSmallDistance()
        rotateDegrees(150)
        tankDrive.on(ev3.SpeedPercent(30), ev3.SpeedPercent(30))
    elif (color == colorSensor.COLOR_BLUE or color == colorSensor.COLOR_YELLOW or color == colorSensor.COLOR_RED) : 
        print("lake with color={color}".format(color=color))
        log("lake")
        tankDrive.stop()
        rotateDegrees(90)
        tankDrive.on(ev3.SpeedPercent(30), ev3.SpeedPercent(30))
    elif checkCollision():
        log("collision")
        tankDrive.stop()
        reverseSmallDistance()
        rotateDegrees(180)
        tankDrive.on(ev3.SpeedPercent(30), ev3.SpeedPercent(30))

