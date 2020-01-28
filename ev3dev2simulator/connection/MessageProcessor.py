from typing import Any, Tuple

from ev3dev2._platform.ev3 import LEDS
from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.MotorCommandProcessor import MotorCommandProcessor
from ev3dev2simulator.connection.message import RotateCommand, StopCommand, SoundCommand, DataRequest, LedCommand
from ev3dev2simulator.state import RobotState
from ev3dev2simulator.util.Util import remove_scaling, apply_scaling

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


    def __init__(self, brick_name: str, robot_state: RobotState):
        cfg = get_config().get_data()
        large_sim_type = get_config().is_large_sim_type()

        self.brick_name = brick_name + ':' if brick_name else ''

        self.pixel_coasting_sub = apply_scaling(cfg['motor_settings']['pixel_coasting_subtraction'])
        self.degree_coasting_sub = cfg['motor_settings']['degree_coasting_subtraction']

        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.address_us_front = cfg['alloc_settings']['ultrasonic_sensor']['front']
        self.address_us_rear = cfg['alloc_settings']['ultrasonic_sensor']['rear'] if large_sim_type else ''

        self.robot_state = robot_state
        self.command_processor = MotorCommandProcessor()
        self.led_cache = {k: None for k in LEDS.values()}


    def process_rotate_command(self, command: RotateCommand) -> float:
        """
        Process the given RotateCommand by creating the appropriate motor jobs in the RobotState. The type of jobs created
        depends on the motor called. The command for the center motor is processed for degrees, while the other motors
        are processed for pixels.
        :param command: to process.
        :return: a floating point value representing the time in seconds the given command will take to execute.
        """

        full_address = self._to_full_address(command.address)
        side = self.robot_state.get_motor_side(full_address)

        if side is None:
            return 0
        else:
            spf, frames, coast_frames, run_time = self._process_rotate_command_values(command, side)

            self.robot_state.clear_motor_jobs(side)

            for i in range(frames):
                self._put_motor_job(spf, side)

            self._process_coast(coast_frames, spf, side)
            return run_time


    def _process_rotate_command_values(self, command: RotateCommand, side: str) -> Tuple[float, int, int, float]:
        """
        Process the given command into the correct movement values.
        :param command: to process.
        :param side: the motor is located.
        :return: a Tuple with the processed values
        """

        if side == 'center':
            dpf, frames, coast_frames, run_time = self.command_processor.process_drive_command_degrees(command)
            return -dpf, frames, coast_frames, run_time
        else:
            return self.command_processor.process_drive_command_pixels(command)


    def process_stop_command(self, command: StopCommand) -> float:
        """
        Process the given stop command by clearing the current motor job queue
        and creating motor coast jobs in the RobotState. The type of jobs created
        depends on the motor called. The command for the center motor is processed for degrees, while the other motors
        are processed for pixels.
        :param command: to process.
        :return: a floating point value representing the time in seconds the given command will take to execute.
        """

        full_address = self._to_full_address(command.address)
        side = self.robot_state.get_motor_side(full_address)

        if side is None:
            return 0
        else:
            spf, frames, run_time = self._process_stop_command_values(command, side)

            self.robot_state.clear_motor_jobs(side)
            self._process_coast(frames, spf, side)
            return run_time


    def _process_stop_command_values(self, command: StopCommand, side: str) -> Tuple[float, int, float]:
        """
        Process the given command into the correct movement values.
        :param command: to process.
        :param side: the motor is located.
        :return: a Tuple with the processed values
        """

        if side == 'center':
            dpf, frames, run_time = self.command_processor.process_stop_command_degrees(command)
            return -dpf, frames, run_time
        else:
            return self.command_processor.process_stop_command_pixels(command)


    def _process_coast(self, frames, ppf, side):
        """
        Process coasting by creating move jobs decreasing in speed in the RobotState.
        :param frames: to coast before coming to a halt.
        :param ppf: speed of motor when the coasting starts.
        :param side: of the motor in the RobotState.
        """

        coasting_sub = self.degree_coasting_sub if side == 'center' else self.pixel_coasting_sub
        og_ppf = ppf

        for i in range(frames):
            if og_ppf > 0:
                ppf = max(ppf - coasting_sub, 0)
            else:
                ppf = min(ppf + coasting_sub, 0)

            self._put_motor_job(ppf, side)


    def process_led_command(self, command: LedCommand):
        """
        Process the given sound command by creating a sound job with a message which can be put on the simulator screen.
        :param command: to process.
        """

        self.led_cache[command.address] = command.brightness
        led_id = command.get_led_id()

        color_tuple = (self.led_cache[led_id + ':red:brick-status'], self.led_cache[led_id + ':green:brick-status'])
        color = LED_COLORS.get(color_tuple)

        if color is not None:
            self.robot_state.set_led_color(self.brick_name, led_id, color)


    def process_sound_command(self, command: SoundCommand):
        """
        Process the given sound command by creating a sound job with a message which can be put on the simulator screen.
        :param command: to process.
        """

        msg_len = len(command.message)
        multiplier = msg_len / 2.5
        frames = int(round(self.frames_per_second * multiplier))

        message = '\n'.join(command.message[i:i + 10] for i in range(0, msg_len, 10))

        for i in range(frames):
            self.robot_state.put_sound_job(message)


    def process_data_request(self, request: DataRequest) -> Any:
        """
        Process the given data request by retrieving the requested value from the RobotState and returning this.
        :param request: to process.
        :return: a dictionary containing the requested value.
        """

        full_address = self._to_full_address(request.address)
        value = self.robot_state.get_value(full_address)

        if request.address == self.address_us_front or request.address == self.address_us_rear:
            return remove_scaling(value)
        else:
            return value


    def _put_motor_job(self, job: float, side: str):
        """
        Add a new move job to the queue for the motor corresponding to the given side.
        :param job: to add.
        :param side: the motor is located.
        """

        if side == 'center':
            self.robot_state.put_center_motor_job(job)
        elif side == 'left':
            self.robot_state.put_left_motor_job(job)
        else:
            self.robot_state.put_right_motor_job(job)


    def _to_full_address(self, address: str):
        return self.brick_name + address
