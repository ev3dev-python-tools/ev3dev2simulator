import unittest

from ev3dev2simulator.config.config import get_simulation_settings, load_config
from ev3dev2simulator.state.MotorCommandProcessor import MotorCommandProcessor
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.StopCommand import StopCommand

# wheel_circumference = 135.7168
wheel_circumference = 175.92918860

class MotorCommandProcessorTest(unittest.TestCase):

    def setUp(self) -> None:
        load_config(None)

    def test_process_drive_command_degrees_hold(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 100, 1000, 'hold')
        # 1000 degrees, 100 per second

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

    def test_process_drive_command_distance_hold(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 100, 1000, 'hold')
        spf, frames, coast_frames, run_time = creator.process_drive_command_distance(command)

        frames_check = 10 * 30  # (1000/100) * 30 # distance * fps
        distance_in_mm = 1000/360 * wheel_circumference
        dpf = distance_in_mm / frames_check
        self.assertAlmostEqual(spf, dpf, 3)
        self.assertEqual(frames, 300)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 10)

    def test_process_drive_command_distance_break(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, -1000, 'break')

        spf, frames, coast_frames, run_time = creator.process_drive_command_distance(command)

        frames_check = 2 * 30  # (-1000/500) * 30 # distance * fps
        distance_in_mm = -1000/360 * wheel_circumference
        dpf = distance_in_mm / frames_check
        self.assertAlmostEqual(spf, dpf, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 0)
        self.assertEqual(run_time, 2)

    def test_process_drive_command_distance_coast(self):
        creator = MotorCommandProcessor()
        command = RotateCommand('ev3-ports:outA', 500, 1000, 'coast')

        spf, frames, coast_frames, run_time = creator.process_drive_command_distance(command)

        frames_check = 2 * 30  # (1000/500) * 30 # distance * fps
        distance_in_mm = 1000/360 * wheel_circumference
        dpf = distance_in_mm / frames_check
        self.assertAlmostEqual(spf, dpf, 3)
        self.assertEqual(frames, 60)
        self.assertEqual(coast_frames, 12)
        self.assertAlmostEqual(run_time, 2.4, 3)

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

    def test_process_stop_command_distance_hold(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 100, 'hold')

        spf, frames, run_time = creator.process_stop_command_distance(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)

    def test_process_stop_command_distance_break(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', -500, 'break')

        spf, frames, run_time = creator.process_stop_command_distance(command)

        self.assertEqual(spf, 0)
        self.assertEqual(frames, 0)
        self.assertEqual(run_time, 0)

    def test_process_stop_command_distance_coast(self):
        creator = MotorCommandProcessor()
        command = StopCommand('ev3-ports:outA', 500, 'coast')
        distance_coasting_sub = 0.7

        spf, frames, run_time = creator.process_stop_command_distance(command)

        mm_per_second = 500/360 * wheel_circumference
        mm_per_frame = mm_per_second / 30  # divide by fps
        frames_check = round(mm_per_frame / distance_coasting_sub)

        self.assertAlmostEqual(spf, mm_per_frame, 3)
        self.assertEqual(frames, frames_check)
        self.assertAlmostEqual(run_time, 0.4, 3)

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
        coasting_sub = get_simulation_settings()['motor_settings']['distance_coasting_subtraction']
        creator = MotorCommandProcessor()

        frames = creator._coast_frames_required(20, coasting_sub)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)

        frames = creator._coast_frames_required(-20, coasting_sub)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)

    def test_to_mm_per_frame(self):
        creator = MotorCommandProcessor()
        mm_check = (wheel_circumference / 360 * 730) / 100
        ppf = creator._to_mm_per_frame(100, 730)
        self.assertAlmostEqual(ppf, mm_check, 3)

        mm_check = (wheel_circumference / 360 * -730) / 100
        ppf = creator._to_mm_per_frame(100, -730)
        self.assertAlmostEqual(ppf, mm_check, 3)

    def test_to_mm(self):
        creator = MotorCommandProcessor()

        mm_check = wheel_circumference / 360 * 720
        mm = creator._to_mm(720)
        self.assertAlmostEqual(mm, mm_check, 3)

        mm_check = wheel_circumference / 360 * -720
        mm = creator._to_mm(-720)
        self.assertAlmostEqual(mm, mm_check, 3)


if __name__ == '__main__':
    unittest.main()
