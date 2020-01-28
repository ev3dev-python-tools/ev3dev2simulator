import json
import threading
import unittest
# based on scaling_multiplier: 0.60
from typing import Any

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.state.RobotState import RobotState


class ServerSocketTest(unittest.TestCase):

    def test_process_drive_command_degrees(self):
        d = {
            'type': 'RotateCommand',
            'address': 'ev3-ports:outA',
            'speed': 10,
            'distance': 100,
            'stop_action': 'hold'
        }

        robot_state = RobotState()
        server = ClientSocketHandler(robot_state, None, 'left_brick')

        data = server._process_drive_command(d)
        val = self._deserialize(data)

        self.assertEqual(10, val)


    def test_process_drive_command_pixels(self):
        d = {
            'type': 'RotateCommand',
            'address': 'ev3-ports:outB',
            'speed': 10,
            'distance': 100,
            'stop_action': 'hold'
        }

        robot_state = RobotState()
        server = ClientSocketHandler(robot_state, None, 'left_brick')

        data = server._process_drive_command(d)
        val = self._deserialize(data)

        self.assertEqual(10, val)


    def test_process_stop_command(self):
        d = {
            'type': 'StopCommand',
            'address': 'ev3-ports:outD',
            'speed': 100,
            'stop_action': 'coast'
        }

        robot_state = RobotState()
        server = ClientSocketHandler(robot_state, None, 'left_brick')

        data = server._process_stop_command(d)
        val = self._deserialize(data)

        self.assertAlmostEqual(0.0667, val, 3)


    def test_process_sound_command(self):
        d = {
            'type': 'SoundCommand',
            'message': 'A test is running at the moment!',
        }

        frames_per_second = get_config().get_data()['exec_settings']['frames_per_second']
        frames = int(round((32 / 2.5) * frames_per_second))
        robot_state = RobotState()

        server = ClientSocketHandler(robot_state, None, 'left_brick')
        server._process_sound_command(d)

        for i in range(frames):
            self.assertIsNotNone(robot_state.next_sound_job())

        self.assertIsNone(robot_state.next_sound_job())


    def test_process_data_request(self):
        d = {
            'type': 'DataRequest',
            'address': 'ev3-ports:in4',
        }

        robot_state = RobotState()
        robot_state.values['left_brick:ev3-ports:in4'] = 10
        robot_state.locks['left_brick:ev3-ports:in4'] = threading.Lock()

        server = ClientSocketHandler(robot_state, None, 'left_brick')
        data = server._process_data_request(d)
        val = self._deserialize(data)

        self.assertEqual(val, 10)


    def _deserialize(self, data: bytes) -> Any:
        """
        Deserialize the given data.
        :param data: to be deserialized.
        :return: any type representing value inside the data.
        """

        val = data.decode()
        obj_dict = json.loads(val)

        return obj_dict['value']


if __name__ == '__main__':
    unittest.main()
