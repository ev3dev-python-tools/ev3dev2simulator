#!/usr/bin/env python3
from time import sleep

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, OUTPUT_B
from ev3dev2.led import Leds
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from testprograms.BluetoothHelper import BluetoothHelper


def reverseRotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotateDegrees(degrees):
    tank_drive.turn_left(SpeedPercent(40), degrees)


def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))

def measurementOn():
    tank_measurement.on_to_position(20, -100)

def measurementOff():
    tank_measurement.on_to_position(20, 100)

def checkColor():
    if cs.color != 1:
        print('gg')
        leds.set_color("RIGHT", "AMBER")
        tank_drive.stop()
        measurementOn()
        measurementOff()
        reverseRotations(1)
        rotateDegrees(180)
        drive()
    else:
        leds.set_color("RIGHT", "GREEN")


def measurement_on():
    tank_measurement.on_to_position(20, -100)


def measurement_off():
    tank_measurement.on_to_position(20, 100)

def check():
    while True:
        checkColor()


bth = BluetoothHelper()
bth.connect_as_server()
bth.send("Hello?")

leds = Leds()

# leds.animate_rainbow()
cs = ColorSensor(INPUT_2)

tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)
tank_measurement = MediumMotor(OUTPUT_B)

drive()
check()
