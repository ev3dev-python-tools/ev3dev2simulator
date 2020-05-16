import os
import sys
import threading
import unittest
from multiprocessing import Process
from time import sleep
from unittest.mock import patch

from ev3dev2.unit import STUD_MM

from ev3dev2.wheel import EV3EducationSetTire

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, OUTPUT_B, SpeedPercent, MoveDifferential, MediumMotor

from ev3dev2simulator import __main__


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_args = ["program", "-t", "config_large"]
        with patch.object(sys, 'argv', test_args):
            sim = Process(target=__main__.main, daemon=True)
            sim.start()

        sleep(4)

    def test_MoveTank(self):
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
        tank_drive.on_for_degrees(10, 50, 720)
        self.assertEqual(tank_drive.is_running, False)

        tank_drive.on(30, 30)
        self.assertEqual(tank_drive.is_running, True)

        sleep(2)
        tank_drive.stop()
        self.assertEqual(tank_drive.is_running, False)

        tank_drive.on_for_seconds(-50, -50, 2, block=False)
        self.assertEqual(tank_drive.is_running, True)

        sleep(3)
        tank_drive.on_for_rotations(50, -50, 1)
        self.assertEqual(tank_drive.is_running, False)

    def test_MoveDifferential(self):
        tank_drive = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)

        tank_drive.turn_right(20, 90 - 34)
        self.assertEqual(tank_drive.is_running, False)

        tank_drive.odometry_start()

        tank_drive.on_to_coordinates(30, -50, 300)
        self.assertEqual(tank_drive.is_running, False)

        tank_drive.on_for_distance(30, 300)
        self.assertEqual(tank_drive.is_running, False)

        tank_drive.on_arc_right(30, 200, 600, block=True)
        self.assertEqual(tank_drive.is_running, False)

    def test_MediumMotor(self):
        tank_measurement = MediumMotor(OUTPUT_B)
        def measurement_on():
            tank_measurement.on_to_position(20, -100)

        def measurement_off():
            tank_measurement.on_to_position(20, 100)

        measurement_on()
        measurement_off()
        measurement_on()
        measurement_off()

if __name__ == '__main__':
    unittest.main()
