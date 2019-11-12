#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound


def checkColor():
    if cs.color == 6:
        s.speak("blyat.wav")


def check():
    while True:
        checkColor()


s = Sound()
cs = ColorSensor(INPUT_2)

check()
