import sys
import unittest

from unittest.mock import MagicMock

from ev3dev2simulator.config.config import load_config

clientSocketModuleMock = MagicMock()
sys.modules['ev3dev2simulator.connection.ClientSocket'] = clientSocketModuleMock
# you cannot import ClientSocket, since that sets up a connection

clientSocketMock = MagicMock()
clientSocketModuleMock.get_client_socket = lambda: clientSocketMock

from ev3dev2.led import Leds


class LedConnectorTest(unittest.TestCase):

    def setUp(self) -> None:
        clientSocketMock.reset_mock()

    def tearDown(self):
        clientSocketMock.reset_mock()

    def test_leds_set_color(self):
        leds = Leds()
        leds.set_color('LEFT', 'AMBER')
        self.assertEqual(len(clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'LedCommand', 'address': 'led0:red:brick-status', 'brightness': 1})
        fn_name, args, kwargs = clientSocketMock.mock_calls[1]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'LedCommand', 'address': 'led0:green:brick-status', 'brightness': 1})


if __name__ == '__main__':
    unittest.main()
