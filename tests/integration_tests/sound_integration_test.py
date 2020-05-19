import os
import sys
import threading
import unittest
from multiprocessing import Process
from time import sleep

import ev3dev2simulator.config.config as config
from unittest.mock import patch, MagicMock

from ev3dev2.sound import Sound
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent

from ev3dev2simulator import __main__


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        sim = Process(target=__main__.main, daemon=True)
        sim.start()

        sleep(4)

    def test_beep(self):
        print('Should beep 4 times, waits before driving')
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.beep()
        sleep(1)

        print('Should beep 4 times, sound plays during driving')
        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
        flip = 1

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        sleep(3)

    def test_speak(self):
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.speak("tests tests tests tests")
        sleep(3)
        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.speak("tests tests tests tests", play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        sleep(3)

    def test_play_tone(self):
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_tone(500, duration=2, volume=50, play_type=1)
        sleep(3)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_tone(500, duration=2, volume=50, play_type=0)
        sleep(3)

    def test_tone(self):
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.tone([
                (392, 350, 100), (492, 350), (292,), ()
            ])
        sleep(3)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.tone([
                (392, 350, 100), (492, 350), (292,), ()
            ], play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        sleep(3)

    def test_play_note(self):
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_note("C4", 0.5)
        sleep(3)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_note("C4", 0.5, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        sleep(3)

    def skip_test_play_file(self):
        flip = 1

        s = Sound()
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        for x in range(2):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_file('inputFiles/bark.wav')
        sleep(3)

        for x in range(4):
            flip *= -1
            tank_drive.on_for_seconds(SpeedPercent(30 * flip), SpeedPercent(30 * flip), 1, True, True)
            s.play_file('inputFiles/bark.wav', play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        sleep(3)

    def test_play_song(self):
        s = Sound()
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


if __name__ == '__main__':
    unittest.main()
