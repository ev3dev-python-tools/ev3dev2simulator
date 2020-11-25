#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound


def reverseRotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotateDegrees(degrees):
    tank_drive.turn_left(SpeedPercent(40), degrees)


def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))


tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)
sound = Sound()

tank_drive.turn_right(30, 360)
drive()
