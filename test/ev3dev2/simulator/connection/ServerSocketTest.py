import json
import threading
import unittest

# based on scaling_multiplier: 0.60
from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.ServerSocket import ServerSocket
from ev3dev2.simulator.state.RobotState import get_robot_state


class ServerSocketTest(unittest.TestCase):

    def test_process_drive_command(self):
        d = {
            'type': 'DriveCommand',
            'address': 'ev3-ports:outA',
            'ppf': 10,
            'frames': 100,
            'frames_coast': 0
        }

        robot_state = get_robot_state()
        server = ServerSocket(robot_state)
        server._process_drive_command(d)

        for i in range(100):
            l, r = robot_state.next_move_jobs()
            self.assertAlmostEqual(l, 6.0, 3)
            self.assertIsNone(r)

        self.assertEqual((None, None), robot_state.next_move_jobs())


    def test_process_stop_command(self):
        d = {
            'type': 'StopCommand',
            'address': 'ev3-ports:outB',
            'ppf': 20,
            'frames': 200,
        }

        robot_state = get_robot_state()

        server = ServerSocket(robot_state)
        server._process_stop_command(d)

        for i in range(200):
            l, r = robot_state.next_move_jobs()
            self.assertIsNotNone(r)

        self.assertEqual((None, None), robot_state.next_move_jobs())


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
            'address': 'ev3-ports:in4',
        }

        robot_state = get_robot_state()
        robot_state.values['ev3-ports:in4'] = 10
        robot_state.locks['ev3-ports:in4'] = threading.Lock()

        server = ServerSocket(robot_state)
        data = server._process_data_request(d)

        jsn = data.decode()
        jsn = jsn.replace('#', '')

        obj_dict = json.loads(jsn)

        self.assertEqual(obj_dict['value'], 10)


if __name__ == '__main__':
    unittest.main()
