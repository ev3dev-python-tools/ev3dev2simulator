#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2
from ev3dev2.led import Leds
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor


def reverse_rotations(rotations):
    tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations)


def rotate_degrees(degrees):
    degrees = degrees * 2
    tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(0), degrees)


def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))


def check_edge():
    if cs.color == 1:
        print('edge found')
        tank_drive.stop()
        tank_drive.on_for_rotations(SpeedPercent(35), SpeedPercent(35), 2)
        reverse_rotations(3)
        rotate_degrees(150)
        drive()


def check():
    while True:
        check_edge()


leds = Leds()
leds.animate_rainbow()
cs = ColorSensor(INPUT_2)
ts1 = TouchSensor(INPUT_1)
ts4 = TouchSensor(INPUT_4)

tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

drive()
check()
