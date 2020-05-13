import unittest

from unittest.mock import MagicMock, patch
from ev3dev2.led import Leds


class LedConnectorTest(unittest.TestCase):

    def test_leds_set_color(self):
        with patch('ev3dev2.DeviceConnector') as DeviceMock:
            with patch('ev3dev2.connector.LedConnector.get_client_socket') as get_client_socketMock:
                mock_instance = MagicMock()
                get_client_socketMock.return_value = mock_instance
                leds = Leds()

                leds.set_color('LEFT', 'AMBER')
                self.assertEqual(len(mock_instance.mock_calls), 2)
                fn_name, args, kwargs = mock_instance.mock_calls[0]
                self.assertEqual(fn_name, 'send_command')
                self.assertDictEqual(args[0].serialize(),
                                     {'type': 'LedCommand', 'address': 'led0:red:brick-status', 'brightness': 1})
                fn_name, args, kwargs = mock_instance.mock_calls[1]
                self.assertDictEqual(args[0].serialize(),
                                     {'type': 'LedCommand', 'address': 'led0:green:brick-status', 'brightness': 1})


if __name__ == '__main__':
    unittest.main()
