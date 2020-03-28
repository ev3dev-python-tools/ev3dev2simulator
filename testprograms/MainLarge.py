#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, OUTPUT_B
from ev3dev2.led import Leds
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3Tire
from testprograms.BluetoothHelper import BluetoothHelper


def reverseRotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotateDegrees(degrees):
    tank_drive.turn_left(SpeedPercent(40), degrees)


def drive():
    tank_drive.on(SpeedPercent(80), SpeedPercent(80))


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
    if cs.color != 1:
        print('gg')
        # leds.set_color("RIGHT", "AMBER")
        tank_drive.stop()
        reverseRotations(1)
        rotateDegrees(180)
        drive()
    # else:
    #     leds.set_color("RIGHT", "GREEN")


def measurement_on():
    tank_measurement.on_to_position(20, -100)


def measurement_off():
    tank_measurement.on_to_position(20, 100)

def check():
    while True:
        # checkCollision()
        checkColor()
        # checkDistance()


# bth = BluetoothHelper()
# bth.connect_as_server()
# bth.send("Hello?")

leds = Leds()
leds.animate_rainbow()
cs = ColorSensor(INPUT_2)
ts1 = TouchSensor(INPUT_1)
ts4 = TouchSensor(INPUT_4)
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 15 * STUD_MM)
tank_measurement = MediumMotor(OUTPUT_B)

drive()
check()
