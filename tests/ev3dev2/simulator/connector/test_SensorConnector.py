import sys
import unittest

from unittest.mock import MagicMock, patch

from ev3dev2._platform.ev3 import INPUT_2
from ev3dev2simulator.config.config import load_config
from ev3dev2.sensor.lego import ColorSensor

load_config(None)


class SensorConnectorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.DeviceMockPatcher = patch('ev3dev2.DeviceConnector')
        self.get_client_socketPatcher = patch('ev3dev2simulator.connector.SensorConnector.get_client_socket')

        self.DeviceMockPatcher.start()
        self.get_client_socketMock = self.get_client_socketPatcher.start()

        self.addCleanup(self.DeviceMockPatcher.stop)
        self.addCleanup(self.get_client_socketPatcher.stop)

        self.clientSocketMock = MagicMock()
        self.get_client_socketMock.return_value = self.clientSocketMock

    def test_leds_set_color(self):
        self.clientSocketMock.send_command.return_value = 3

        sensor = ColorSensor(INPUT_2)
        val = sensor.value()
        self.assertEqual(val, 3)
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'DataRequest', 'address': 'ev3-ports:in2'})

        val2 = sensor.value()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        self.assertEqual(val, val2)


if __name__ == '__main__':
    unittest.main()
