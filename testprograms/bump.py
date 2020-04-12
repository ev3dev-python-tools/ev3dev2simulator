#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_2, OUTPUT_B
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound

def reverseRotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotateDegrees(degrees):
    tank_drive.turn_left(SpeedPercent(40), degrees)


def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))

def checkColor():
    if cs.color != 6:
        tank_drive.stop()
        sound.speak('gg', play_type=1)
        reverseRotations(1)
        rotateDegrees(80)
        drive()


def measurement_on():
    tank_measurement.on_to_position(20, -100)


def measurement_off():
    tank_measurement.on_to_position(20, 100)

def check():
    while True:
        checkColor()


cs = ColorSensor(INPUT_2)

tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)
tank_measurement = MediumMotor(OUTPUT_B)
sound = Sound()

tank_drive.turn_right(30, 90)
drive()
check()
