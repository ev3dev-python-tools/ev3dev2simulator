import json
import threading
import unittest
# based on scaling_multiplier: 0.60
from typing import Any

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.state.RobotSimulator import RobotState, RobotSimulator


def create_robot_sim():
    config = {'center_x': 0,
              'center_y': 0,
              'name': 'test_bot',
              'parts': [
                  {
                      'name': 'brick-left',
                      'type': 'brick',
                      'brick': '0',
                      'x_offset': '-39',
                      'y_offset': '-22.5'},
                  {
                      'name': 'motor-left',
                      'type': 'motor',
                      'x_offset': '-60',
                      'y_offset': '0.01',
                      'brick': '0',
                      'port': 'ev3-ports:outA'
                  },
                  {
                      'name': 'motor-right',
                      'type': 'motor',
                      'x_offset': '60',
                      'y_offset': '0.01',
                      'brick': '0',
                      'port': 'ev3-ports:outD'
                  },
                  {
                      'name': 'measurement-probe',
                      'type': 'arm',
                      'x_offset': '15',
                      'y_offset': '102',
                      'brick': '0',
                      'port': 'ev3-ports:outB'}
              ]
              }

    robot_state = RobotState(config)
    robot_sim = RobotSimulator(robot_state)
    return ClientSocketHandler(robot_sim, None, 0, 'left_brick')


class ServerSocketTest(unittest.TestCase):

    def test_process_drive_command_degrees(self):
        d = {
            'type': 'RotateCommand',
            'address': 'ev3-ports:outA',
            'speed': 10,
            'distance': 100,
            'stop_action': 'hold'
        }

        server = create_robot_sim()
        data = server.message_handler._process_drive_command(d)
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

        server = create_robot_sim()

        data = server.message_handler._process_drive_command(d)
        val = self._deserialize(data)

        self.assertEqual(10, val)

    def test_process_stop_command(self):
        d = {
            'type': 'StopCommand',
            'address': 'ev3-ports:outD',
            'speed': 100,
            'stop_action': 'coast'
        }

        server = create_robot_sim()

        data = server.message_handler._process_stop_command(d)
        val = self._deserialize(data)

        self.assertAlmostEqual(0.0667, val, 3)

    def test_process_sound_command(self):
        d = {
            'type': 'SoundCommand',
            'message': 'A test is running at the moment!',
            'duration': 2,
            'soundType': 'speak'
        }

        frames_per_second = get_config().get_visualisation_config()['exec_settings']['frames_per_second']
        frames = int(2 * frames_per_second)

        server = create_robot_sim()
        server.message_handler._process_sound_command(d)

        for i in range(frames):
            soundJob = [i[1] for i in server.robot_sim.next_actuator_jobs() if i[0] == (0, 'speaker')][0]
            self.assertIsNotNone(soundJob)
        soundJob = [i[1] for i in server.robot_sim.next_actuator_jobs() if i[0] == (0, 'speaker')][0]
        self.assertIsNone(soundJob)

    def test_process_data_request(self):
        d = {
            'type': 'DataRequest',
            'address': 'ev3-ports:in4',
        }

        server = create_robot_sim()
        server.robot_sim.robot.values[(0, 'ev3-ports:in4')] = 10
        server.robot_sim.locks[(0, 'ev3-ports:in4')] = threading.Lock()
        data = server.message_handler._process_data_request(d)
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
