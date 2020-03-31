import threading
import unittest

from ev3dev2simulator.config.config import get_simulation_settings, load_config
from ev3dev2simulator.state.MessageProcessor import MessageProcessor
from ev3dev2simulator.connection.message.DataRequest import DataRequest
from ev3dev2simulator.connection.message.LedCommand import LedCommand
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand

from tests.ev3dev2.simulator.connection.test_ServerSocket import create_robot_sim

load_config(None)
wheel_circumference = 175.92918860

class MessageProcessorTest(unittest.TestCase):

    def test_create_jobs_center(self):
        robot_sim = create_robot_sim()

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outB', 20, 100, 'hold'))

        for i in range(150):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[3][1], -0.667, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[1][1])
            self.assertIsNone(jobs[2][1])

        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_create_jobs_left(self):
        robot_sim = create_robot_sim()

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outA', 1, 100, 'hold'))

        frames_check = 100 * 30  # (1000/100) * 30 # distance * fps
        distance_in_mm = 100 / 360 * wheel_circumference
        dpf = distance_in_mm / frames_check

        for i in range(3000):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[1][1], dpf, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[2][1])
            self.assertIsNone(jobs[3][1])

        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_create_jobs_right(self):
        robot_sim = create_robot_sim()

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outD', 10, 100, 'hold'))

        frames_check = 10 * 30  # (1000/100) * 30 # distance * fps
        distance_in_mm = 100 / 360 * wheel_circumference
        dpf = distance_in_mm / frames_check

        for i in range(frames_check):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[2][1], dpf, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[1][1])
            self.assertIsNone(jobs[3][1])
        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_create_jobs_coast_center(self):
        coasting_sub = get_simulation_settings()['motor_settings']['degree_coasting_subtraction']
        robot_sim = create_robot_sim()

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outB', 80, 200, 'coast'))

        for i in range(75):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[3][1], -2.667, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[1][1])
            self.assertIsNone(jobs[2][1])

        ppf = 2.667 - coasting_sub
        for i in range(2):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[3][1], -ppf, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[1][1])
            self.assertIsNone(jobs[2][1])
            ppf = max(ppf - coasting_sub, 0)

        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_create_jobs_coast_left(self):
        coasting_sub = get_simulation_settings()['motor_settings']['distance_coasting_subtraction']
        robot_sim = create_robot_sim()

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_rotate_command(RotateCommand('ev3-ports:outA', 80, 200, 'coast'))

        frames_check = (200/80) * 30  # (1000/100) * 30 # distance * fps
        distance_in_mm = 200 / 360 * wheel_circumference
        dpf = distance_in_mm / frames_check

        for i in range(75):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[1][1], dpf, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[2][1])
            self.assertIsNone(jobs[3][1])

        ppf = dpf - coasting_sub
        for i in range(2):
            jobs = robot_sim.next_actuator_jobs()
            self.assertAlmostEqual(jobs[1][1], ppf, 3)
            self.assertIsNone(jobs[0][1])
            self.assertIsNone(jobs[3][1])
            self.assertIsNone(jobs[2][1])
            ppf = max(ppf - coasting_sub, 0)

        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_process_sound_command(self):
        robot_sim = create_robot_sim()

        frames_per_second = get_simulation_settings()['exec_settings']['frames_per_second']
        frames = int(5 * frames_per_second)

        message_processor = MessageProcessor(0, robot_sim)
        message_processor.process_sound_command(SoundCommand('A test is running at the moment!', 5, 'speak'))

        for i in range(frames - 1):
            soundJob = [i[1] for i in robot_sim.next_actuator_jobs() if i[0] == (0, 'speaker')][0]
            self.assertIsNotNone(soundJob)

        message = [i[1] for i in robot_sim.next_actuator_jobs() if i[0] == (0, 'speaker')][0]
        self.assertEqual(message, 'A test is \nrunning at\n the momen\nt!')

        jobs = robot_sim.next_actuator_jobs()
        self.assertEqual((jobs[0][1], jobs[1][1], jobs[2][1], jobs[3][1]), (None, None, None, None))

    def test_process_led_command(self):
        robot_sim = create_robot_sim()
        message_processor = MessageProcessor(0, robot_sim)

        command1 = LedCommand('led0:red:brick-status', 1)
        command2 = LedCommand('led0:green:brick-status', 1)

        message_processor.process_led_command(command1)
        message_processor.process_led_command(command2)

        self.assertEqual(robot_sim.robot.led_colors[(0, 'led0')], 0)
        self.assertEqual(robot_sim.robot.led_colors[(0, 'led1')], 1)

        command3 = LedCommand('led1:red:brick-status', 1)
        command4 = LedCommand('led1:green:brick-status', 0.5)

        message_processor.process_led_command(command3)
        message_processor.process_led_command(command4)

        self.assertEqual(robot_sim.robot.led_colors[(0, 'led0')], 0)
        self.assertEqual(robot_sim.robot.led_colors[(0, 'led1')], 4)

    def test_process_data_request(self):
        robot_sim = create_robot_sim()
        robot_sim.robot.values[(1, 'ev3-ports:in4')] = 10
        robot_sim.locks[(1, 'ev3-ports:in4')] = threading.Lock()

        message_processor = MessageProcessor(1, robot_sim)
        value = message_processor.process_data_request(DataRequest('ev3-ports:in4'))

        self.assertEqual(value, 10)


if __name__ == '__main__':
    unittest.main()
