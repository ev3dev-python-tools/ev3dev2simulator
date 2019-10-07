import threading
import unittest

from ev3dev2.connection.message.DataRequest import DataRequest
from ev3dev2.connection.message.DriveCommand import DriveCommand
from ev3dev2.connection.message.SoundCommand import SoundCommand
from simulator.connection.MessageProcessor import MessageProcessor
from simulator.state.RobotState import get_robot_state
from simulator.util.Util import load_config, apply_scaling


# based on scaling_multiplier: 0.60
class MessageProcessorTest(unittest.TestCase):

    def test_create_jobs_left(self):
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('ev3-ports:outA', 1.2, 100, 0))

        for i in range(100):
            l, r = robot_state.next_move_jobs()
            self.assertAlmostEqual(l, 0.72, 3)
            self.assertIsNone(r)

        self.assertEqual((None, None), robot_state.next_move_jobs())


    def test_create_jobs_right(self):
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('ev3-ports:outB', 0.8, 150, 0))

        for i in range(150):
            l, r = robot_state.next_move_jobs()
            self.assertIsNone(l)
            self.assertAlmostEqual(r, 0.48, 3)

        self.assertEqual((None, None), robot_state.next_move_jobs())


    def test_create_jobs_coast(self):
        coasting_sub = apply_scaling(load_config()['wheel_settings']['coasting_subtraction'])
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('ev3-ports:outA', 0.4, 100, 1))

        for i in range(100):
            l, r = robot_state.next_move_jobs()
            self.assertAlmostEqual(l, 0.24, 3)
            self.assertIsNone(r)

        ppf = 0.24 - coasting_sub
        for i in range(1):
            l, r = robot_state.next_move_jobs()
            self.assertAlmostEqual(l, ppf, 3)
            self.assertIsNone(r)
            ppf -= coasting_sub

        self.assertEqual((None, None), robot_state.next_move_jobs())


    def test_process_sound_command(self):
        robot_state = get_robot_state()

        frames_per_second = load_config()['exec_settings']['frames_per_second']
        frames = int(round((32 / 2.5) * frames_per_second))

        message_processor = MessageProcessor(robot_state)
        message_processor.process_sound_command(SoundCommand('A test is running at the moment!'))

        for i in range(frames - 1):
            self.assertIsNotNone(robot_state.next_sound_job())

        message = robot_state.next_sound_job()
        self.assertEqual(message, 'A test is \nrunning at\n the momen\nt!')
        self.assertIsNone(robot_state.next_sound_job())


    def test_process_data_request(self):
        robot_state = get_robot_state()
        robot_state.values['ev3-ports:in4'] = 10
        robot_state.locks['ev3-ports:in4'] = threading.Lock()

        message_processor = MessageProcessor(robot_state)
        value = message_processor.process_data_request(DataRequest('ev3-ports:in4'))

        self.assertEqual(value, 10)


if __name__ == '__main__':
    unittest.main()
