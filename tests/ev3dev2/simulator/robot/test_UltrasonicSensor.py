import unittest
from unittest.mock import MagicMock

from pymunk import Space

from ev3dev2simulator.config.config import load_config
from ev3dev2simulator.robotpart.UltrasonicSensorTop import UltrasonicSensor

load_config(None)


class TestUltraSonicSensor(unittest.TestCase):
    def test_distance_no_obstacle(self):
        config = {
            'name': 'ultrasonic-sensor-front',
            'type': 'ultrasonic_sensor',
            'x_offset': 0,
            'y_offset': -91.5,
            'brick': 0,
            'port': 'ev3-ports:in3'
        }
        robot = MagicMock()
        us = UltrasonicSensor(config, robot)
        us.setup_pymunk_shape(1, None)
        us.sprite = MagicMock()
        us.sprite.angle = 0
        space = Space()
        val = us.distance(space)
        self.assertEqual(val, 2550)


if __name__ == '__main__':
    unittest.main()
