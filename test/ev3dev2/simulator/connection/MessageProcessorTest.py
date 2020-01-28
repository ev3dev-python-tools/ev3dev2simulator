import threading
import unittest

# based on scaling_multiplier: 0.60
from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.MessageProcessor import MessageProcessor
from ev3dev2simulator.connection.message.DataRequest import DataRequest
from ev3dev2simulator.connection.message.LedCommand import LedCommand
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand
from ev3dev2simulator.state.RobotState import RobotState
from ev3dev2simulator.util.Util import apply_scaling


class MessageProcessorTest(unittest.TestCase):

    def test_create_jobs_center(self):
        robot_state = RobotState()

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outB', 20, 100, 'hold'))

        for i in range(150):
            c, l, r = robot_state.next_motor_jobs()
            self.assertAlmostEqual(c, -0.667, 3)
            self.assertIsNone(l)
            self.assertIsNone(r)

        self.assertEqual((None, None, None), robot_state.next_motor_jobs())


    def test_create_jobs_left(self):
        robot_state = RobotState()

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outA', 1, 100, 'hold'))

        for i in range(3000):
            c, l, r = robot_state.next_motor_jobs()
            self.assertIsNone(c)
            self.assertAlmostEqual(l, 0.010, 3)
            self.assertIsNone(r)

        self.assertEqual((None, None, None), robot_state.next_motor_jobs())


    def test_create_jobs_right(self):
        robot_state = RobotState()

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outD', 10, 100, 'hold'))

        for i in range(300):
            c, l, r = robot_state.next_motor_jobs()
            self.assertIsNone(c)
            self.assertIsNone(l)
            self.assertAlmostEqual(r, 0.104, 3)

        self.assertEqual((None, None, None), robot_state.next_motor_jobs())


    def test_create_jobs_coast_center(self):
        coasting_sub = get_config().get_data()['motor_settings']['degree_coasting_subtraction']
        robot_state = RobotState()

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outB', 80, 200, 'coast'))

        for i in range(75):
            c, l, r = robot_state.next_motor_jobs()
            self.assertAlmostEqual(c, -2.667, 3)
            self.assertIsNone(l)
            self.assertIsNone(r)

        ppf = 2.667 - coasting_sub
        for i in range(2):
            c, l, r = robot_state.next_motor_jobs()
            self.assertAlmostEqual(c, -ppf, 3)
            self.assertIsNone(l)
            self.assertIsNone(r)
            ppf = max(ppf - coasting_sub, 0)

        self.assertEqual((None, None, None), robot_state.next_motor_jobs())


    def test_create_jobs_coast_left(self):
        coasting_sub = apply_scaling(get_config().get_data()['motor_settings']['pixel_coasting_subtraction'])
        robot_state = RobotState()

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outA', 80, 200, 'coast'))

        for i in range(75):
            c, l, r = robot_state.next_motor_jobs()
            self.assertIsNone(c)
            self.assertAlmostEqual(l, 0.833, 3)
            self.assertIsNone(r)

        ppf = 0.833 - coasting_sub
        for i in range(2):
            c, l, r = robot_state.next_motor_jobs()
            self.assertIsNone(c)
            self.assertAlmostEqual(l, ppf, 3)
            self.assertIsNone(r)
            ppf = max(ppf - coasting_sub, 0)

        self.assertEqual((None, None, None), robot_state.next_motor_jobs())


    def test_process_sound_command(self):
        robot_state = RobotState()

        frames_per_second = get_config().get_data()['exec_settings']['frames_per_second']
        frames = int(round((32 / 2.5) * frames_per_second))

        message_processor = MessageProcessor('left_brick', robot_state)
        message_processor.process_sound_command(SoundCommand('A test is running at the moment!'))

        for i in range(frames - 1):
            self.assertIsNotNone(robot_state.next_sound_job())

        message = robot_state.next_sound_job()
        self.assertEqual(message, 'A test is \nrunning at\n the momen\nt!')
        self.assertIsNone(robot_state.next_sound_job())


    def test_process_left_led_command(self):
        robot_state = RobotState()
        message_processor = MessageProcessor('right_brick', robot_state)

        command1 = LedCommand('led0:red:brick-status', 1)
        command2 = LedCommand('led0:green:brick-status', 1)

        message_processor.process_led_command(command1)
        message_processor.process_led_command(command2)

        self.assertEqual(robot_state.right_brick_left_led_color, 0)
        self.assertEqual(robot_state.right_brick_right_led_color, 1)

        command3 = LedCommand('led1:red:brick-status', 1)
        command4 = LedCommand('led1:green:brick-status', 0.5)

        message_processor.process_led_command(command3)
        message_processor.process_led_command(command4)

        self.assertEqual(robot_state.right_brick_left_led_color, 0)
        self.assertEqual(robot_state.right_brick_right_led_color, 4)


    def test_process_right_led_command(self):
        robot_state = RobotState()
        message_processor = MessageProcessor('right_brick', robot_state)

        command1 = LedCommand('led0:red:brick-status', 1)
        command2 = LedCommand('led0:green:brick-status', 1)

        message_processor.process_led_command(command1)
        message_processor.process_led_command(command2)

        self.assertEqual(robot_state.right_brick_left_led_color, 0)
        self.assertEqual(robot_state.right_brick_right_led_color, 1)

        command3 = LedCommand('led1:red:brick-status', 1)
        command4 = LedCommand('led1:green:brick-status', 0.5)

        message_processor.process_led_command(command3)
        message_processor.process_led_command(command4)

        self.assertEqual(robot_state.right_brick_left_led_color, 0)
        self.assertEqual(robot_state.right_brick_right_led_color, 4)


    def test_process_data_request(self):
        robot_state = RobotState()
        robot_state.values['right_brick:ev3-ports:in4'] = 10
        robot_state.locks['right_brick:ev3-ports:in4'] = threading.Lock()

        message_processor = MessageProcessor('right_brick', robot_state)
        value = message_processor.process_data_request(DataRequest('ev3-ports:in4'))

        self.assertEqual(value, 10)


if __name__ == '__main__':
    unittest.main()
