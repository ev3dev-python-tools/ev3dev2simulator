import sys
import unittest
from time import sleep

from unittest.mock import MagicMock

from ev3dev2._platform.ev3 import OUTPUT_A

class MotorConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clientSocketModuleMock = MagicMock()
        sys.modules['ev3dev2simulator.connection.ClientSocket'] = cls.clientSocketModuleMock
        # you cannot import ClientSocket, since that sets up a connection

        cls.clientSocketMock = MagicMock()
        cls.clientSocketModuleMock.get_client_socket = lambda: cls.clientSocketMock

    @classmethod
    def tearDownClass(cls) -> None:
        del sys.modules['ev3dev2simulator.connection.ClientSocket']

    def tearDown(self):
        self.clientSocketMock.reset_mock()

    def test_run_timed(self):
        from ev3dev2.motor import Motor
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
        from ev3dev2.motor import Motor
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
        from ev3dev2.motor import Motor
        motor = Motor(OUTPUT_A)
        self.clientSocketMock.send_command.return_value = 0
        motor.on(0, False)
        motor.stop()
        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)
        self.assertEqual(motor.speed_sp, 0)

    def test_stop_reverse(self):
        from ev3dev2.motor import Motor
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
        from ev3dev2.motor import Motor
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
        from ev3dev2.motor import Motor
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
