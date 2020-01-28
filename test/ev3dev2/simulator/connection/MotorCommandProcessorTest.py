import unittest

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.MotorCommandProcessor import MotorCommandProcessor
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.StopCommand import StopCommand


class MotorCommandProcessorTest(unittest.TestCase):

    def test_process_drive_command_degrees_hold(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 100, 1000, 'hold')

        spf, frames, coast_frames, run_time = creator.process_drive_command_degrees(command)

        self.assertAlmostEqual(spf, 3.333, 3)
        self.assertEqual(frames, 300)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 10)


    def test_process_drive_command_degrees_break(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, -1000, 'break')

        spf, frames, coast_frames, run_time = creator.process_drive_command_degrees(command)

        self.assertAlmostEqual(spf, -16.667, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 2)


    def test_process_drive_command_degrees_coast(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, 1000, 'coast')

        spf, frames, coast_frames, run_time = creator.process_drive_command_degrees(command)

        self.assertAlmostEqual(spf, 16.667, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 11)
        self.assertAlmostEqual(run_time, 2.367, 3)


    def test_process_drive_command_pixels_hold(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 100, 1000, 'hold')

        spf, frames, coast_frames, run_time = creator.process_drive_command_pixels(command)

        self.assertAlmostEqual(spf, 1.041, 3)
        self.assertEqual(frames, 300)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 10)


    def test_process_drive_command_pixels_break(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, -1000, 'break')

        spf, frames, coast_frames, run_time = creator.process_drive_command_pixels(command)

        self.assertAlmostEqual(spf, -5.206, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 2)


    def test_process_drive_command_pixels_coast(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, 1000, 'coast')

        spf, frames, coast_frames, run_time = creator.process_drive_command_pixels(command)

        self.assertAlmostEqual(spf, 5.206, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 11)
        self.assertAlmostEqual(run_time, 2.367, 3)


    def test_process_stop_command_degrees_hold(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 100, 'hold')

        spf, frames, run_time = creator.process_stop_command_degrees(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)


    def test_process_stop_command_degrees_break(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', -500, 'break')

        spf, frames, run_time = creator.process_stop_command_degrees(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)


    def test_process_stop_command_degrees_coast(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 500, 'coast')

        spf, frames, run_time = creator.process_stop_command_degrees(command)

        self.assertAlmostEqual(spf, 16.667, 3)
        self.assertEqual(frames, 11)
        self.assertAlmostEqual(run_time, 0.367, 3)


    def test_process_stop_command_pixels_hold(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 100, 'hold')

        spf, frames, run_time = creator.process_stop_command_pixels(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)


    def test_process_stop_command_pixels_break(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', -500, 'break')

        spf, frames, run_time = creator.process_stop_command_pixels(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)


    def test_process_stop_command_pixels_coast(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 500, 'coast')

        spf, frames, run_time = creator.process_stop_command_pixels(command)

        self.assertAlmostEqual(spf, 5.206, 3)
        self.assertEqual(frames, 11)
        self.assertAlmostEqual(run_time, 0.367, 3)


    def test_frames_required(self):
        creator = MotorCommandProcessor()

        frames = creator._frames_required(20, 100)
        self.assertEqual(frames, 150)

        frames = creator._frames_required(20, -100)
        self.assertEqual(frames, 150)

        frames = creator._frames_required(33, 1000)
        self.assertEqual(frames, 909)

        frames = creator._frames_required(-33, 1000)
        self.assertEqual(frames, 909)

        frames = creator._frames_required(-66, -700)
        self.assertEqual(frames, 318)


    def test_coast_frames_required(self):
        coasting_sub = get_config().get_data()['motor_settings']['pixel_coasting_subtraction']
        creator = MotorCommandProcessor()

        frames = creator._coast_frames_required(20, coasting_sub)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)

        frames = creator._coast_frames_required(-20, coasting_sub)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)


    def test_to_pixels_per_frame(self):
        creator = MotorCommandProcessor()

        ppf = creator._to_pixels_per_frame(100, 730)
        self.assertAlmostEqual(ppf, 2.280, 3)

        ppf = creator._to_pixels_per_frame(100, -730)
        self.assertAlmostEqual(ppf, -2.280, 3)


    def test_to_pixels(self):
        # ran with scaling 0.7
        creator = MotorCommandProcessor()

        pixels = creator._to_pixels(720)
        self.assertAlmostEqual(pixels, 224.9, 3)

        pixels = creator._to_pixels(-720)
        self.assertAlmostEqual(pixels, -224.9, 3)


if __name__ == '__main__':
    unittest.main()
