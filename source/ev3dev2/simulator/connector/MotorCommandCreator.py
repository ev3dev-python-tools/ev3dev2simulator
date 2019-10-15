from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.ClientSocket import get_client_socket
from ev3dev2.simulator.connection.message.DriveCommand import DriveCommand
from ev3dev2.simulator.connection.message.StopCommand import StopCommand


class MotorCommandCreator:
    """
    The MotorCommandCreator class is responsible for creating movement jobs for the simulated robot.
    These jobs are processed by the simulator every update. The Python Arcade library used
    for the simulator provides a logic update every frame. Meaning 'frames_per_second' number of jobs
    are processed per second.
    """


    def __init__(self):
        cfg = load_config()

        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.wheel_circumference = cfg['wheel_settings']['circumference']
        self.coasting_sub = cfg['wheel_settings']['coasting_subtraction']

        self.client_socket = get_client_socket()


    def create_drive_command(self, speed: float, distance: float, stop_action: str, address: str) -> float:
        """
        Create the command required to rotate the motor at the address for a distance at a speed.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :param stop_action: of the motor, this can be 'hold', 'break' or 'coast'.
        :param address: of the motor to create a command for.
        """

        frames = self._frames_required(speed, distance)
        ppf = self._to_pixels_per_frame(frames, distance)

        if stop_action == 'coast':
            coast_frames = self._coast_frames_required(ppf)
            self._create_drive_command(frames, coast_frames, ppf, address)

            return (frames + coast_frames) / self.frames_per_second
        else:
            self._create_drive_command(frames, 0, ppf, address)
            return frames / self.frames_per_second


    def create_stop_command(self, speed: float, stop_action: str, address: str) -> float:
        """
        Create the command required to stop the motor at the address.
        :param speed: in degrees per second the motor is traveling when stopped.
        :param stop_action: of the motor, this can be 'hold', 'break' or 'coast'.
        :param address: of the motor to create a stop command for.
        """

        ppf = self._to_pixels(speed) / self.frames_per_second

        if stop_action == 'coast':
            frames = self._coast_frames_required(ppf)
            self._create_stop_command(frames, ppf, address)

            return frames / self.frames_per_second
        else:
            self._create_stop_command(0, 0, address)
            return 0


    def _frames_required(self, speed: float, distance: float) -> int:
        """
        Calculate the number of frames required to rotate a motor for a distance at a speed.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return: an integer representing the number of frames.
        """

        seconds = abs(distance) / abs(speed)
        return int(round(seconds * self.frames_per_second))


    def _coast_frames_required(self, speed: float) -> int:
        """
        Calculate the number of frames required for a motor to coast to a halt based on the given speed.
        :param speed: in degrees per second.
        :return: an integer representing the number of frames.
        """

        pos_speed = abs(speed)
        return int(round(pos_speed / self.coasting_sub))


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

        return self.wheel_circumference * (distance / 360)


    def _create_drive_command(self, frames: int, coast_frames: int, ppf: float, address: str):
        """
        Create and send a DriveCommand to move the motor for a distance for a number of frames.
        Also include a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param frames: amount for which this command lasts.
        :param ppf: speed in pixels per frame before coasting starts.
        :param address: of the motor to create a command for.
        """

        command = DriveCommand(address, ppf, frames, coast_frames)
        self.client_socket.send_motor_command(command)


    def _create_stop_command(self, frames: int, ppf: float, address: str):
        """
        Create and send a StopCommand to stop the motor.
        Also include a number of frames for coasting speed subtraction. These frames allow
        for the travel distance to decrease bit by bit until the motor does not move anymore.
        :param frames: amount for which this command lasts.
        :param ppf: current speed of the motor.
        :param address: of the motor to create a command for.
        """

        command = StopCommand(address, ppf, frames)
        self.client_socket.send_motor_command(command)


motor_command_creator = MotorCommandCreator()


def get_motor_command_creator():
    return MotorCommandCreator()
