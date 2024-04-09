"""
The message_processor module contains the class MessageProcessor.
This class takes the commands given and converts them into jobs the robot simulator understands.
"""

from typing import Any, Tuple
# noinspection PyProtectedMember
from ev3dev2._platform.ev3 import LEDS
from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.state.motor_command_processor import MotorCommandProcessor
from ev3dev2simulator.state.robot_simulator import RobotSimulator

from ev3dev2simulator.connection.message.config_request import ConfigRequest
from ev3dev2simulator.connection.message.rotate_command import RotateCommand
from ev3dev2simulator.connection.message.stop_command import StopCommand
from ev3dev2simulator.connection.message.sound_command import SoundCommand
from ev3dev2simulator.connection.message.led_command import LedCommand
from ev3dev2simulator.connection.message.data_request import DataRequest


LED_COLORS = dict()
LED_COLORS[(1, 1)] = 0  # Amber
LED_COLORS[(0, 0)] = 1  # Black
LED_COLORS[(1, 0)] = 2  # Red
LED_COLORS[(0, 1)] = 3  # Green
LED_COLORS[(1, 0.5)] = 4  # Orange
LED_COLORS[(0.1, 1)] = 5  # Yellow


class MessageProcessor:
    """
    Class used for processing the messages (requests/commands) received by the socket of the simulator and relaying
    them to the RobotState.
    """

    def __init__(self, brick_id: int, robot_sim: RobotSimulator):
        cfg = get_simulation_settings()

        self.brick_id = brick_id

        self.distance_coasting_sub = float(cfg['motor_settings']['distance_coasting_subtraction'])
        self.degree_coasting_sub = float(cfg['motor_settings']['degree_coasting_subtraction'])
        self.frames_per_second = int(cfg['exec_settings']['frames_per_second'])

        self.robot_sim = robot_sim
        self.motor_command_processor = MotorCommandProcessor()
        self.led_cache = {k: None for k in LEDS.values()}

    def process_rotate_command(self, command: RotateCommand) -> float:
        """
        Process the given RotateCommand by creating the appropriate motor jobs in the RobotState.
        The type of jobs created  depends on the motor called.
        The command for the arm motor is processed for degrees, while the other motors are processed for distance.
        :param command: to process.
        :return: a floating point value representing the time in seconds the given command will take to execute.
        """

        full_address = self._to_full_address(command.address)
        motor = self.robot_sim.robot.get_actuator(full_address)
        spf, frames, coast_frames, run_time = self._process_rotate_command_values(command, motor)

        self.robot_sim.clear_actuator_jobs(full_address)

        for _ in range(frames):
            self.robot_sim.put_actuator_job(full_address, spf)

        self._process_coast(coast_frames, spf, motor)
        return run_time

    def _process_rotate_command_values(self, command: RotateCommand, motor: any) -> Tuple[float, int, int, float]:
        """
        Process the given command into the correct movement values.
        :param command: to process.
        :param motor: the motor.
        :return: a Tuple with the processed values
        """

        if motor.ev3type == 'arm':
            dpf, frames, coast_frames, run_time = self.motor_command_processor.process_drive_command_degrees(command)
            return -dpf, frames, coast_frames, run_time
        return self.motor_command_processor.process_drive_command_distance(command)

    def process_stop_command(self, command: StopCommand) -> float:
        """
        Process the given stop command by clearing the current motor job queue
        and creating motor coast jobs in the RobotState. The type of jobs created
        depends on the motor called. The command for the center motor is processed for degrees, while the other motors
        are processed for distance.
        :param command: to process.
        :return: a floating point value representing the time in seconds the given command will take to execute.
        """

        full_address = self._to_full_address(command.address)
        motor = self.robot_sim.robot.get_actuator(full_address)

        spf, frames, run_time = self._process_stop_command_values(command, motor)

        self.robot_sim.clear_actuator_jobs(full_address)
        self._process_coast(frames, spf, motor)
        return run_time

    def _process_stop_command_values(self, command: StopCommand, motor: any) -> Tuple[float, int, float]:
        """
        Process the given command into the correct movement values.
        :param command: to process.
        :param motor: the motor.
        :return: a Tuple with the processed values
        """

        if motor.ev3type == 'arm':
            dpf, frames, run_time = self.motor_command_processor.process_stop_command_degrees(command)
            return -dpf, frames, run_time
        return self.motor_command_processor.process_stop_command_distance(command)

    def _process_coast(self, frames, ppf, motor):
        """
        Process coasting by creating move jobs decreasing in speed in the RobotState.
        :param frames: to coast before coming to a halt.
        :param ppf: speed of motor when the coasting starts.
        :param motor: the motor in the RobotState.
        """

        coasting_sub = self.degree_coasting_sub if motor.ev3type == 'arm' else self.distance_coasting_sub
        og_ppf = ppf

        for _ in range(frames):
            if og_ppf > 0:
                ppf = max(ppf - coasting_sub, 0)
            else:
                ppf = min(ppf + coasting_sub, 0)
            self.robot_sim.put_actuator_job(self._to_full_address(motor.address), ppf)

    def process_led_command(self, command: LedCommand):
        """
        Process the given sound command by creating a sound job with a message which can be put on the simulator screen.
        :param command: to process.
        """

        self.led_cache[command.address] = command.brightness
        led_id = command.get_led_id()

        color_tuple = (self.led_cache[led_id + ':red:brick-status'], self.led_cache[led_id + ':green:brick-status'])
        color = self._red_green_to_color(color_tuple)
        if color is not None:
            self.robot_sim.set_led_color(self.brick_id, led_id, color)

    @staticmethod
    def _red_green_to_color(color_tuple):
        if len(color_tuple) != 2:
            return None
        if color_tuple[0] is None:
            color_tuple = (0, color_tuple[1])
        if color_tuple[1] is None:
            color_tuple = (color_tuple[0], 0)

        color = LED_COLORS.get(color_tuple)
        diff = 2
        if color is None:
            for key, value in LED_COLORS.items():
                new_diff = abs(color_tuple[0] - key[0]) + abs(color_tuple[1] - key[1])
                if new_diff < diff:
                    color = value
                    diff = new_diff
        return color

    def process_sound_command(self, command: SoundCommand):
        """
        Process the given sound command by creating a sound job with a message. This job is handled
        by putting a message on the simulator screen.

        The modified ev3dev2 API does play the sound on the client side. The simulator itself does not play
        any sounds.

        :param command: to process.
        """
        frames = int(round(self.frames_per_second * command.duration))
        msg_len = len(command.message)
        message = '\n'.join(command.message[i:i + 10] for i in range(0, msg_len, 10))
        for i in range(frames):
            self.robot_sim.put_actuator_job(self._to_full_address('speaker'), message)

    def process_data_request(self, request: DataRequest) -> Any:
        """
        Process the given data request by retrieving the requested value from the RobotState and returning this.
        :param request: to process.
        :return: a dictionary containing the requested value.
        """
        full_address = self._to_full_address(request.address)
        return self.robot_sim.get_value(full_address)

    def process_config_request(self, request: ConfigRequest) -> Any:
        """
        Process the given data request by retrieving the port of the device from the RobotState and returning this.
        :param request: to process.
        :return: a dictionary containing the requested value.
        """
        return self.robot_sim.determine_port(self.brick_id, request.kwargs, request.class_name)

    def _to_full_address(self, address: str):
        return self.brick_id, address
