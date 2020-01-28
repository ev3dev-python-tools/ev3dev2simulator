from typing import Tuple

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.StopCommand import StopCommand


class MotorCommandProcessor:
    """
    The MotorCommandProcessor class is responsible for processing the movement jobs from the ev3dev2 mock.
    These jobs are converted to values the simulator can use for its robot.
    """


    def __init__(self):
        cfg = get_config().get_data()

        self.scaling_multiplier = get_config().get_scale()
        self.pixel_coasting_sub = cfg['motor_settings']['pixel_coasting_subtraction'] * self.scaling_multiplier
        self.degree_coasting_sub = cfg['motor_settings']['degree_coasting_subtraction']

        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.wheel_circumference = cfg['wheel_settings']['circumference']


    def process_drive_command_degrees(self, command: RotateCommand) -> Tuple[float, int, int, float]:
        """
        Process the given RotateCommand which moves the motor for a distance for a number of frames.
        This is done by calculating degree values per frame and the number of frames required for the command to complete.
        Also calculate a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param command: to process.
        :return: a Tuple with the processed values
        """

        frames = self._frames_required(command.speed, command.distance)
        dpf = command.distance / frames

        if command.stop_action == 'coast':
            coast_frames = self._coast_frames_required(dpf, self.degree_coasting_sub)
            run_time = self._to_seconds(frames + coast_frames)

        else:
            coast_frames = 0
            run_time = self._to_seconds(frames)

        return dpf, frames, coast_frames, run_time


    def process_drive_command_pixels(self, command: RotateCommand) -> Tuple[float, int, int, float]:
        """
        Process the given RotateCommand which moves the motor for a distance for a number of frames.
        This is done by calculating pixel values per frame and the number of frames required for the command to complete.
        Also calculate a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param command: to process.
        :return: a Tuple with the processed values
        """

        frames = self._frames_required(command.speed, command.distance)
        ppf = self._to_pixels_per_frame(frames, command.distance)

        if command.stop_action == 'coast':
            coast_frames = self._coast_frames_required(ppf, self.pixel_coasting_sub)
            run_time = self._to_seconds(frames + coast_frames)

        else:
            coast_frames = 0
            run_time = self._to_seconds(frames)

        return ppf, frames, coast_frames, run_time


    def process_stop_command_degrees(self, command: StopCommand) -> Tuple[float, int, float]:
        """
        Process the given StopCommand to stop the motor.
        Also include a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param command: to process.
        :return: a Tuple with the processed values
        """

        dpf = command.speed / self.frames_per_second

        if command.stop_action == 'coast':
            frames = self._coast_frames_required(dpf, self.degree_coasting_sub)
            run_time = self._to_seconds(frames)

            return dpf, frames, run_time

        return 0, 0, 0


    def process_stop_command_pixels(self, command: StopCommand) -> Tuple[float, int, float]:
        """
        Process the given StopCommand to stop the motor.
        Also include a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param command: to process.
        :return: a Tuple with the processed values
        """

        ppf = self._to_pixels(command.speed) / self.frames_per_second

        if command.stop_action == 'coast':
            frames = self._coast_frames_required(ppf, self.pixel_coasting_sub)
            run_time = self._to_seconds(frames)

            return ppf, frames, run_time

        return 0, 0, 0


    def _frames_required(self, speed: float, distance: float) -> int:
        """
        Calculate the number of frames required to rotate a motor for a distance at a speed.
        A minimum of one frame is returned otherwise actions taking less than a frame would not be processed further.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return: an integer representing the number of frames.
        """

        seconds = abs(distance) / abs(speed)
        frames = int(round(seconds * self.frames_per_second))

        return max(frames, 1)


    def _coast_frames_required(self, speed: float, coasting_sub: float) -> int:
        """
        Calculate the number of frames required for a motor to coast to a halt based on the given speed.
        :param speed: in pixels per second.
        :return: an integer representing the number of frames.
        """

        pos_speed = abs(speed)
        return int(round(pos_speed / coasting_sub))


    def _to_pixels_per_frame(self, frames: int, distance: float) -> float:
        """
        Calculate the number of pixels required per frame to rotate a motor a distance within frames.
        :param frames: available.
        :param distance: in degrees.
        :return: an floating point number representing the number of pixels per frame.
        """

        pixel_distance = self._to_pixels(distance)
        return pixel_distance / frames


    def _to_pixels(self, distance: float) -> float:
        """
        Convert a distance in degrees to a distance in pixels. Calculation is done
        based on the circumference of the wheel attached to the motor.
        :param distance: in degrees.
        :return: an integer representing the distance in pixels.
        """

        return self.wheel_circumference * (distance / 360) * self.scaling_multiplier


    def _to_seconds(self, frames: int) -> float:
        """
        Convert the number of frames into number of seconds.
        :param frames: to convert
        :return: a floating point value representing the number of frames
        """

        return frames / self.frames_per_second
