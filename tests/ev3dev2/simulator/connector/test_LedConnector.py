import sys
import unittest

from unittest.mock import MagicMock


class LedConnectorTest(unittest.TestCase):

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

    def test_leds_set_color(self):

        from ev3dev2.led import Leds
        leds = Leds()

        leds.set_color('LEFT', 'AMBER')
        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'LedCommand', 'address': 'led0:red:brick-status', 'brightness': 1})
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'LedCommand', 'address': 'led0:green:brick-status', 'brightness': 1})
        self.clientSocketMock.reset_mock()


if __name__ == '__main__':
    unittest.main()
