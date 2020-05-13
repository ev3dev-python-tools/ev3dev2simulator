import sys
import unittest
from time import sleep

from unittest.mock import MagicMock, patch

from ev3dev2._platform.ev3 import OUTPUT_A
from ev3dev2.motor import Motor


class MotorConnectorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.DeviceMockPatcher = patch('ev3dev2.DeviceConnector')
        self.get_client_socketPatcher = patch('ev3dev2.connector.MotorConnector.get_client_socket')

        self.DeviceMockPatcher.start()
        self.get_client_socketMock = self.get_client_socketPatcher.start()

        self.addCleanup(self.DeviceMockPatcher.stop)
        self.addCleanup(self.get_client_socketPatcher.stop)

        self.clientSocketMock = MagicMock()
        self.get_client_socketMock.return_value = self.clientSocketMock

    def test_run_timed(self):
        self.clientSocketMock.send_command.return_value = 1
        motor = Motor(OUTPUT_A)
        motor.on_for_seconds(30, 1)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'RotateCommand', 'address': 'ev3-ports:outA', 'stop_action': 'hold',
                              'speed': 315, 'distance': 315.0})

    def test_direct_on_and_stop(self):
        self.clientSocketMock.send_command.return_value = 1

        motor = Motor(OUTPUT_A)
        motor.on(10)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        distance = 105 * 45
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'RotateCommand', 'address': 'ev3-ports:outA', 'stop_action': 'hold',
                              'speed': 105, 'distance': distance})

        motor.stop()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'StopCommand', 'address': 'ev3-ports:outA', 'stop_action': 'hold',
                              'speed': 105})

    def test_stop_with_no_speed(self):
        motor = Motor(OUTPUT_A)
        self.clientSocketMock.send_command.return_value = 0
        motor.on(0, False)
        motor.stop()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        self.assertEqual(motor.speed_sp, 0)

    def test_stop_reverse(self):
        motor = Motor(OUTPUT_A)
        self.clientSocketMock.send_command.return_value = 0
        motor.on(-10, False)
        motor.stop()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'StopCommand', 'address': 'ev3-ports:outA', 'stop_action': 'coast',
                              'speed': 105})

    def test_run_to_rel_pos(self):
        self.clientSocketMock.send_command.return_value = 1

        motor = Motor(OUTPUT_A)
        motor.on_for_degrees(30, 30, False)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'RotateCommand', 'address': 'ev3-ports:outA', 'stop_action': 'coast',
                              'speed': 315, 'distance': 30})

    def test_run_direct(self):
        self.clientSocketMock.send_command.return_value = 1

        motor = Motor(OUTPUT_A)
        motor.duty_cycle_sp = 30
        motor.stop_action = 'coast'
        motor.run_direct()

        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'RotateCommand', 'address': 'ev3-ports:outA', 'stop_action': 'coast',
                              'speed': 315, 'distance': 14175.0})


if __name__ == '__main__':
    unittest.main()
