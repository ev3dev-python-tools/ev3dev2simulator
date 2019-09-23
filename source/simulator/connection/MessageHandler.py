from ev3dev2.connection import MotorCommand, DataRequest
from simulator.util.Util import load_config


class MessageHandler:

    def __init__(self, robot_state):
        cfg = load_config()
        self.address_motor_center = cfg['alloc_settings']['motor']['center']
        self.address_motor_left = cfg['alloc_settings']['motor']['left']
        self.address_motor_right = cfg['alloc_settings']['motor']['right']

        self.coasting_sub = cfg['wheel_settings']['coasting_subtraction']

        self.robot_state = robot_state


    def handle_motor_command(self, command: MotorCommand):
        ppf = command.ppf
        side = self._get_motor_side(command.address)

        for i in range(command.frames):
            if side == 'left':
                self.robot_state.put_left_move_job(ppf)
            else:
                self.robot_state.put_right_move_job(ppf)

        for i in range(command.frames_coast):
            ppf = max(ppf - self.coasting_sub, 0)

            if side == 'left':
                self.robot_state.put_left_move_job(ppf)
            else:
                self.robot_state.put_right_move_job(ppf)


    def handle_data_request(self, request: DataRequest):
        return self.robot_state.d[request.address]


    def _get_motor_side(self, address: str) -> str:
        """
        Get the location of the motor on the actual robot based on its address.
        :param address: of the motor
        :return 'center', 'left' or 'right'
        """

        if self.address_motor_center == address:
            return 'center'

        if self.address_motor_left == address:
            return 'left'

        if self.address_motor_right == address:
            return 'right'
