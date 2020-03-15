#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2
from ev3dev2.led import Leds
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from testprograms.BluetoothHelper import BluetoothHelper

def reverseRotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotateDegrees(degrees):
    degrees = degrees * 2
    tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(0), degrees)


def drive(speed):
    tank_drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(speed), 2, True)


def checkCollision():
    if ts1.is_pressed or ts4.is_pressed:
        print('gg')
        # leds.set_color("LEFT", "YELLOW")
        tank_drive.stop()

        reverseRotations(1)
        rotateDegrees(180)

        drive()
    # else:
    #     leds.set_color("LEFT", "RED")


def checkColor():
    if cs.color == 6:
        print('gg')
        # leds.set_color("RIGHT", "AMBER")
        tank_drive.stop()

        reverseRotations(1)
        rotateDegrees(150)

        drive()
    # else:
    #     leds.set_color("RIGHT", "GREEN")


def check():
    while True:
        # checkCollision()
        checkColor()
        # checkDistance()


# bth = BluetoothHelper()
# bth.connect_as_server()
# bth.send("Hello?")

leds = Leds()
leds.animate_rainbow(duration=111111, block=False)
cs = ColorSensor(INPUT_2)
ts1 = TouchSensor(INPUT_1)
ts4 = TouchSensor(INPUT_4)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

drive(30)
drive(-30)
check()
