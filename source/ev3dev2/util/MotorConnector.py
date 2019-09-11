from ev3dev2.util.Singleton import Singleton
from simulator.util.Util import load_config

#: See MockMotor for variable explanation
COMMAND_RUN_FOREVER = 'run-forever'
COMMAND_RUN_TO_ABS_POS = 'run-to-abs-pos'
COMMAND_RUN_TO_REL_POS = 'run-to-rel-pos'
COMMAND_RUN_TIMED = 'run-timed'
COMMAND_RUN_DIRECT = 'run-direct'


class MotorConnector(metaclass=Singleton):

    def __init__(self):
        cfg = load_config()
        self.address_motor_left = cfg['motor_alloc']['left_motor']
        self.address_motor_right = cfg['motor_alloc']['right_motor']
        self.address_motor_center = cfg['motor_alloc']['center_motor']

        self.dict = {}
        self.speed_left = 0
        self.speed_right = 0
        self.speed_center = 0

        self.degrees_left = 0
        self.degrees_right = 0
        self.degrees_center = 0

        self.pid_left = 0
        self.pid_right = 0

    def _get_motor_side(self, address):
        if self.address_motor_left == address:
            return 'left'

        if self.address_motor_right == address:
            return 'right'

        if self.address_motor_center == address:
            return 'center'

    def set_speed(self, address, speed):
        print(address + " SPEED: " + str(speed))

        side = self._get_motor_side(address)
        self.dict['speed_' + side] = speed

    def set_degrees(self, address, degrees):
        print(address + " DISTANCE: " + str(degrees))

        side = self._get_motor_side(address)
        self.dict['distance_' + side] = degrees

    def execute(self, address, pid, command):
        if pid == 0:

            if COMMAND_RUN_FOREVER == command:
                self.run_forever(address)
            elif COMMAND_RUN_TO_ABS_POS == command:
                self.run_to_abs_pos(address)

        else:
            self.execute_dual(address, pid, command)

    def execute_dual(self, address, pid, command):
        if self.address_motor_left == address and self.pid_right == pid \
                or self.address_motor_right == address and self.pid_left == pid:
            pass

    def run_forever(self, address):
        pass

    def run_to_abs_pos(self, address):

        pass
