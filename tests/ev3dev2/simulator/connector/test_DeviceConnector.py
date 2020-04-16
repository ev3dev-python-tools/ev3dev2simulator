import unittest
from unittest.mock import patch, MagicMock

from ev3dev2 import auto as ev3, DeviceNotFound
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2simulator.config.config import load_config

load_config(None)


class TestDeviceConnector(unittest.TestCase):

    def test_give_existing_port(self):
        with patch('ev3dev2simulator.connector.DeviceConnector.get_client_socket') as Device_get_client_socketMock:
            with patch('ev3dev2simulator.connector.SensorConnector.get_client_socket') as get_client_socketMock:
                mock_instance = MagicMock()
                Device_get_client_socketMock.return_value = mock_instance
                mock_instance.send_command.return_value = 'ev3-ports:in3'

                us = UltrasonicSensor(ev3.INPUT_1)
                self.assertEqual(us.address, 'ev3-ports:in3')

    def test_give_non_existing_port(self):
        with patch('ev3dev2simulator.connector.DeviceConnector.get_client_socket') as Device_get_client_socketMock:
            with patch('ev3dev2simulator.connector.SensorConnector.get_client_socket') as get_client_socketMock:
                mock_instance = MagicMock()
                Device_get_client_socketMock.return_value = mock_instance
                mock_instance.send_command.return_value = 'dev_not_connected'

                self.assertRaises(DeviceNotFound, UltrasonicSensor, ev3.INPUT_1)

    def test_determine_connected_port(self):
        with patch('ev3dev2simulator.connector.DeviceConnector.get_client_socket') as Device_get_client_socketMock:
            with patch('ev3dev2simulator.connector.SensorConnector.get_client_socket') as get_client_socketMock:
                mock_instance = MagicMock()
                Device_get_client_socketMock.return_value = mock_instance
                mock_instance.send_command.return_value = 'ev3-ports:in1'

                us = UltrasonicSensor()
                self.assertEqual(us.address, 'ev3-ports:in1')
                self.assertEqual(us.connector.address, 'ev3-ports:in1')

    def test_determine_disconnected_port(self):
        with patch('ev3dev2simulator.connector.DeviceConnector.get_client_socket') as Device_get_client_socketMock:
            with patch('ev3dev2simulator.connector.SensorConnector.get_client_socket') as get_client_socketMock:
                mock_instance = MagicMock()
                Device_get_client_socketMock.return_value = mock_instance
                mock_instance.send_command.return_value = 'dev_not_connected'

                self.assertRaises(DeviceNotFound, UltrasonicSensor)

if __name__ == '__main__':
    unittest.main()
