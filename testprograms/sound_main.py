#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_3, INPUT_2
from ev3dev2.led import Leds
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep

flip = 1


def drive():
    global flip
    flip = flip * -1
    tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)


s = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

for x in range(4):
    drive()
    s.beep()
sleep(1)

for x in range(4):
    drive()
    s.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
sleep(3)

for x in range(4):
    drive()
    s.speak("testjes tests tests tests")
sleep(3)
for x in range(4):
    drive()
    s.speak("testjes tests tests tests", play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
sleep(3)

for x in range(4):
    drive()
    s.play_tone(500, duration=2, volume=50, play_type=1)
sleep(3)

for x in range(4):
    drive()
    s.play_tone(500, duration=2, volume=50, play_type=0)
sleep(3)


for x in range(4):
    drive()
    s.tone([
        (392, 350, 100), (492, 350), (292,), ()
    ])
sleep(3)

for x in range(4):
    drive()
    s.tone([
        (392, 350, 100), (492, 350), (292,), ()
    ], play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
sleep(3)

for x in range(4):
    drive()
    s.play_note("C4", 0.5)
sleep(3)

for x in range(4):
    drive()
    s.play_note("C4", 0.5, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
sleep(3)

for x in range(2):
    drive()
    s.play_file('inputFiles/bark.wav')
sleep(3)

for x in range(4):
    drive()
    s.play_file('inputFiles/bark.wav', play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
sleep(3)

s.play_song((
    ('D4', 'e3'),  # intro anacrouse
    ('D4', 'e3'),
    ('D4', 'e3'),
    ('G4', 'h'),  # meas 1
    ('D5', 'h'),
    ('C5', 'e3'),  # meas 2
    ('B4', 'e3'),
    ('A4', 'e3'),
    ('G5', 'h'),
    ('D5', 'q'),
    ('C5', 'e3'),  # meas 3
    ('B4', 'e3'),
    ('A4', 'e3'),
    ('G5', 'h'),
    ('D5', 'q'),
    ('C5', 'e3'),  # meas 4
    ['B4', 'e3'],
    ('C5', 'e3'),
    ('A4', 'h.'),
))
