import os
import sys
import threading
import unittest
from multiprocessing import Process
from time import sleep
from unittest.mock import patch
from ev3dev2.led import Leds, Led

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
        my_leds = Leds()
        my_leds.set_color('LEFT', (0.5, 0.3))
        my_leds.set_color('RIGHT', 'AMBER')
        sleep(2)
        my_leds.all_off()
        my_leds.animate_cycle(('RED', 'GREEN', 'AMBER'), duration=5)

    def test_ledsOff(self):
        my_leds = Leds()
        my_leds.set_color('LEFT', (0.5, 0.3))
        my_leds.set_color('RIGHT', 'AMBER')
        sleep(5)
        my_leds.all_off()
        sleep(5)

if __name__ == '__main__':
    unittest.main()
