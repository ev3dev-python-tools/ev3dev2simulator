#!/usr/bin/env python3
from time import sleep

from ev3dev2 import auto as ev3

# initialize
# ------------

# initialize sensors
us = ev3.UltrasonicSensor()
led = ev3.Leds()
button = ev3.Button()
speaker = ev3.Sound()
speaker.beep()
print(us.address)
sleep(5)

