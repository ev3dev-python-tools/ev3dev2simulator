import sys
import unittest
from time import sleep

from unittest.mock import MagicMock, patch

from ev3dev2._platform.ev3 import INPUT_2, INPUT_1
from ev3dev2simulator.config.config import load_config
from ev3dev2.sensor.lego import ColorSensor, TouchSensor

load_config(None)


class SensorConnectorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.DeviceMockPatcher = patch('ev3dev2simulator.connector.DeviceConnector.get_client_socket')
        self.get_client_socketPatcher = patch('ev3dev2simulator.connector.SensorConnector.get_client_socket')

        self.get_device_client_socketMock = self.DeviceMockPatcher.start()
        self.get_client_socketMock = self.get_client_socketPatcher.start()

        self.addCleanup(self.DeviceMockPatcher.stop)
        self.addCleanup(self.get_client_socketPatcher.stop)

        self.deviceClientSocketMock = MagicMock()
        self.get_device_client_socketMock.return_value = self.deviceClientSocketMock

        self.clientSocketMock = MagicMock()
        self.get_client_socketMock.return_value = self.clientSocketMock

    def test_color_sensor(self):
        self.deviceClientSocketMock.send_command.return_value = 'ev3-ports:in2'
        self.clientSocketMock.send_command.return_value = 3

        sensor = ColorSensor(INPUT_2)
        val = sensor.color
        self.assertEqual(val, 3)
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'DataRequest', 'address': 'ev3-ports:in2'})

        val2 = sensor.value()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        self.assertEqual(val, val2)

        val = sensor.rgb
        self.assertEqual(val, (0, 216, 0))  # assumes 400 is max val, but we use 255 as max
        self.clientSocketMock.send_command.return_value = 6
        sleep(0.1)  # sleep to wait for cache

        sensor.calibrate_white()

        sleep(0.1)  # sleep to wait for cache

        self.clientSocketMock.send_command.return_value = 3
        sleep(0.1)  # sleep to wait for cache
        val = sensor.rgb
        self.assertEqual((0, 255, 0), val)  # Now calibrated to 255



    def test_touch_sensor(self):
        self.deviceClientSocketMock.send_command.return_value = 'ev3-ports:in1'
        self.clientSocketMock.send_command.return_value = True

        sensor = TouchSensor(INPUT_1)
        val = sensor.value()
        self.assertEqual(val, 1)
        self.assertTrue(isinstance(val, int))
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'DataRequest', 'address': 'ev3-ports:in1'})

        val2 = sensor.value()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        self.assertEqual(val, val2)


if __name__ == '__main__':
    unittest.main()
