#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_2, OUTPUT_B, INPUT_4, INPUT_3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import UltrasonicSensor

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

def check():
    while True:
        checkColor()


cs = ColorSensor()

tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)
sound = Sound()
us = UltrasonicSensor()
us.mode = 'US-DIST-CM'

tank_drive.turn_right(30, 90)
drive()
check()
