import json
import unittest

from simulator.connection.ServerSocket import ServerSocket
from simulator.state.RobotState import get_robot_state
from simulator.util.Util import load_config


class ServerSocketTest(unittest.TestCase):

    def test_process_drive_command(self):
        d = {
            'type': 'DriveCommand',
            'address': 'OUTPUT_A',
            'ppf': 10,
            'frames': 100,
            'frames_coast': 0
        }

        robot_state = get_robot_state()
        server = ServerSocket(robot_state)
        server._process_drive_command(d)

        for i in range(100):
            job = robot_state.next_left_move_job()
            self.assertAlmostEqual(job, 10.0, 3)

        self.assertIsNone(robot_state.next_left_move_job())
        self.assertIsNone(robot_state.next_right_move_job())


    def test_process_stop_command(self):
        d = {
            'type': 'StopCommand',
            'address': 'OUTPUT_B',
            'ppf': 20,
            'frames': 200,
        }

        robot_state = get_robot_state()

        server = ServerSocket(robot_state)
        server._process_stop_command(d)

        for i in range(200):
            self.assertIsNotNone(robot_state.next_right_move_job())

        self.assertIsNone(robot_state.next_left_move_job())
        self.assertIsNone(robot_state.next_right_move_job())


    def test_process_sound_command(self):
        d = {
            'type': 'SoundCommand',
            'message': 'A test is running at the moment!',
        }

        frames_per_second = load_config()['exec_settings']['frames_per_second']
        frames = int(round((32 / 2.5) * frames_per_second))
        robot_state = get_robot_state()

        server = ServerSocket(robot_state)
        server._process_sound_command(d)

        for i in range(frames):
            self.assertIsNotNone(robot_state.next_sound_job())

        self.assertIsNone(robot_state.next_sound_job())


    def test_process_data_request(self):
        d = {
            'type': 'DataRequest',
            'address': 'INPUT_4',
        }

        robot_state = get_robot_state()
        robot_state.values['INPUT_4'] = 10

        server = ServerSocket(robot_state)
        data = server._process_data_request(d)

        jsn = data.decode()
        jsn = jsn.replace('#', '')

        obj_dict = json.loads(jsn)

        self.assertEqual(obj_dict['value'], 10)


if __name__ == '__main__':
    unittest.main()
