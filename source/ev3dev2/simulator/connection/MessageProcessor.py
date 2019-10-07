from typing import Any

from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.message import DriveCommand, StopCommand, SoundCommand, DataRequest
from ev3dev2.simulator.util.Util import apply_scaling, remove_scaling


class MessageProcessor:
    """
    Class used for processing the messages (requests/commands) received by the socket of the simulator and relaying
    them to the RobotState.
    """


    def __init__(self, robot_state):
        cfg = load_config()
        self.coasting_sub = apply_scaling(cfg['wheel_settings']['coasting_subtraction'])
        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.address_us = cfg['alloc_settings']['ultrasonic_sensor']['top']

        self.robot_state = robot_state


    def process_drive_command(self, command: DriveCommand):
        """
        Process the given drive command by creating motor move and coast jobs in the RobotState.
        :param command: to process.
        """

        ppf = apply_scaling(command.ppf)
        side = self.robot_state.get_motor_side(command.address)

        for i in range(command.frames):
            self.robot_state.put_move_job(ppf, side)

        self._process_coast(command.frames_coast, ppf, side)


    def process_stop_command(self, command: StopCommand):
        """
        Process the given stop command by clearing the current move job queue
         and creating motor coast jobs in the RobotState.
        :param command: to process.
        """

        ppf = apply_scaling(command.ppf)
        side = self.robot_state.get_motor_side(command.address)
        self.robot_state.clear_move_jobs(side)

        if command.frames != 0:
            self._process_coast(command.frames, ppf, side)


    def _process_coast(self, frames, ppf, side):
        """
        Process coasting by creating move jobs decreasing in speed in the RobotState.
        :param frames: to coast before coming to a halt.
        :param ppf: speed of motor when the coasting starts.
        :param side: of the motor in the RobotState.
        """

        og_ppf = ppf

        for i in range(frames):
            if og_ppf > 0:
                ppf = max(ppf - self.coasting_sub, 0)
            else:
                ppf = min(ppf + self.coasting_sub, 0)

            self.robot_state.put_move_job(ppf, side)


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

        value = self.robot_state.get_value(request.address)

        if request.address == self.address_us:
            return remove_scaling(value)
        else:
            return value
