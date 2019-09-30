import unittest

from ev3dev2.connection.message.DataRequest import DataRequest
from ev3dev2.connection.message.DriveCommand import DriveCommand
from ev3dev2.connection.message.SoundCommand import SoundCommand
from simulator.connection.MessageProcessor import MessageProcessor
from simulator.state.RobotState import get_robot_state
from simulator.util.Util import load_config


class MessageProcessorTest(unittest.TestCase):

    def test_create_jobs_left(self):
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('OUTPUT_A', 0.106, 100, 0))

        for i in range(100):
            job = robot_state.next_left_move_job()
            self.assertAlmostEqual(job, 0.106, 3)

        self.assertIsNone(robot_state.next_left_move_job())
        self.assertIsNone(robot_state.next_right_move_job())


    def test_create_jobs_right(self):
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('OUTPUT_B', 0.426, 150, 0))

        for i in range(150):
            job = robot_state.next_right_move_job()
            self.assertAlmostEqual(job, 0.426, 3)

        self.assertIsNone(robot_state.next_left_move_job())
        self.assertIsNone(robot_state.next_right_move_job())


    def test_create_jobs_coast(self):
        coasting_sub = load_config()['wheel_settings']['coasting_subtraction']
        robot_state = get_robot_state()

        message_processor = MessageProcessor(robot_state)
        message_processor.process_drive_command(DriveCommand('OUTPUT_A', 0.106, 100, 1))

        for i in range(100):
            job = robot_state.next_left_move_job()
            self.assertAlmostEqual(job, 0.106, 3)

        ppf = 0.106 - coasting_sub
        for i in range(1):
            job = robot_state.next_left_move_job()
            self.assertAlmostEqual(job, ppf, 3)
            ppf -= coasting_sub

        self.assertIsNone(robot_state.next_left_move_job())
        self.assertIsNone(robot_state.next_right_move_job())


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
        robot_state.values['INPUT_4'] = 10

        message_processor = MessageProcessor(robot_state)
        value = message_processor.process_data_request(DataRequest('INPUT_4'))

        self.assertEqual(value, 10)


if __name__ == '__main__':
    unittest.main()
