#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound
from testprograms.BluetoothHelper import BluetoothHelper


def checkDistance():
    if -1 > us.value() < 180:
        s.speak("blyat.wav")


def check():
    while True:
        checkDistance()


s = Sound()

bth = BluetoothHelper()
bth.connect_as_client()

us = UltrasonicSensor(INPUT_4)
us.mode = 'US-DIST-CM'

check()
