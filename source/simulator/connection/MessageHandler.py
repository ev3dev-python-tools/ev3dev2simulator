from ev3dev2.connection import DriveCommand, DataRequest, StopCommand
from simulator.util.Util import load_config


class MessageHandler:

    def __init__(self, robot_state):
        cfg = load_config()
        self.coasting_sub = cfg['wheel_settings']['coasting_subtraction']

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


    def handle_data_request(self, request: DataRequest):
        return self.robot_state.d[request.address]
