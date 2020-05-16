import os
import sys
import threading
import unittest
from multiprocessing import Process
from time import sleep
from unittest.mock import patch

from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor, TouchSensor

from ev3dev2.unit import STUD_MM

from ev3dev2.wheel import EV3EducationSetTire

from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2, INPUT_3, INPUT_4

from ev3dev2simulator import __main__


class TestConfig(unittest.TestCase):

    def test_color_and_us_sensor_downwards(self):
        test_args = ["program", "-t", "config_large"]
        with patch.object(sys, 'argv', test_args):
            sim = Process(target=__main__.main, daemon=True)
            sim.start()

        sleep(4)

        clm = ColorSensor(INPUT_2)
        usb = UltrasonicSensor(INPUT_4)
        usb.mode = "US-DIST-CM"
        tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)

        self.assertEqual(clm.value(), 1)
        tank_drive.on_for_rotations(0, -55, 1)
        tank_drive.on_for_rotations(10, 0, 0.2)
        tank_drive.stop()
        self.assertEqual(clm.value(), 5)
        tank_drive.turn_left(30, -40)
        self.assertEqual(usb.value(), 20.0)
        tank_drive.turn_left(30, 120)
        self.assertEqual(usb.value(), 2550.0)

    def test_touch_and_us_sensor_forward(self):
        test_args = ["program", "-t", "config_small"]
        with patch.object(sys, 'argv', test_args):
            sim = Process(target=__main__.main, daemon=True)
            sim.start()

        sleep(4)

        ts1 = TouchSensor(INPUT_1)
        usf = UltrasonicSensor(INPUT_3)
        usf.mode = "US-DIST-CM"
        tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)
        tank_drive.turn_right(30, 90)
        self.assertEqual(ts1.is_pressed, 0)
        sleep(0.2)
        self.assertAlmostEqual(usf.value(), 810, delta=20)
        val = usf.value()
        print(val)
        tank_drive.on_for_distance(50, 600)
        self.assertAlmostEqual(val - 600, usf.value(), delta=20)
        self.assertEqual(False, ts1.is_pressed)
        sleep(3)
        tank_drive.on_for_rotations(20, 0, 0.3)
        self.assertEqual(True, ts1.is_pressed)



if __name__ == '__main__':
    unittest.main()
