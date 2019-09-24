from ev3dev2.connection.message import DriveCommand, DataRequest, StopCommand, SoundCommand
from simulator.util.Util import load_config


class MessageHandler:

    def __init__(self, robot_state):
        cfg = load_config()
        self.coasting_sub = cfg['wheel_settings']['coasting_subtraction']
        self.frames_per_second = cfg['exec_settings']['frames_per_second']

        self.robot_state = robot_state


    def handle_drive_command(self, command: DriveCommand):
        side = self.robot_state.get_motor_side(command.address)

        for i in range(command.frames):
            self.robot_state.put_move_job(command.ppf, side)

        self._handle_coast(command.frames_coast, command.ppf, side)


    def handle_stop_command(self, command: StopCommand):
        side = self.robot_state.get_motor_side(command.address)
        self.robot_state.clear_move_jobs(side)

        if command.frames != 0:
            self._handle_coast(command.frames, command.ppf, side)


    def _handle_coast(self, frames, ppf, side):
        og_ppf = ppf

        for i in range(frames):
            if og_ppf > 0:
                ppf = max(ppf - self.coasting_sub, 0)
            else:
                ppf = min(ppf + self.coasting_sub, 0)

            self.robot_state.put_move_job(ppf, side)


    def handle_sound_command(self, command: SoundCommand):
        msg_len = len(command.message)
        multiplier = msg_len / 5
        frames = int(round(self.frames_per_second * multiplier))

        message = '\n'.join(command.message[i:i + 10] for i in range(0, msg_len, 10))

        for i in range(frames):
            self.robot_state.put_sound_job(message)


    def handle_data_request(self, request: DataRequest):
        return self.robot_state.values[request.address]
