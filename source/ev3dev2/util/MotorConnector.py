from ev3dev2.util.Singleton import Singleton
from simulator.job.JobCreator import JobCreator
from simulator.util.Util import load_config

#: See MockMotor for variable explanation
COMMAND_RUN_FOREVER = 'run-forever'
COMMAND_RUN_TO_ABS_POS = 'run-to-abs-pos'
COMMAND_RUN_TO_REL_POS = 'run-to-rel-pos'
COMMAND_RUN_TIMED = 'run-timed'
COMMAND_RUN_DIRECT = 'run-direct'


class MotorConnector(metaclass=Singleton):

    def __init__(self, job_handler):
        cfg = load_config()
        self.address_motor_left = cfg['motor_alloc_settings']['left_motor']
        self.address_motor_right = cfg['motor_alloc_settings']['right_motor']
        self.address_motor_center = cfg['motor_alloc_settings']['center_motor']

        self.dict = {}

        self.pid_left = 0
        self.pid_right = 0

        self.job_creator = JobCreator(job_handler)

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

    def execute(self, address, command, pid=0):
        if pid == 0:
            self.execute_single(address, command)
        else:
            self.execute_dual(address, command, pid)

    def execute_single(self, address, command):

        if COMMAND_RUN_FOREVER == command:
            self.run_forever(address)
        elif COMMAND_RUN_TO_ABS_POS == command:
            self.run_to_abs_pos(address)
        elif COMMAND_RUN_TO_REL_POS == command:
            self.run_to_rel_pos(address)

    def execute_dual(self, address, command, pid):
        if self.address_motor_left == address and self.pid_right == pid \
                or self.address_motor_right == address and self.pid_left == pid:

            if COMMAND_RUN_FOREVER == command:
                self.run_forever(address)
            elif COMMAND_RUN_TO_ABS_POS == command:
                self.run_to_abs_pos_dual()

    def run_forever(self, address):
        pass

    def run_to_abs_pos(self, address):
        side = self._get_motor_side(address)

        self.job_creator.create_single_job_left(
            self.dict['speed_' + side],
            self.dict['distance_' + side])

    def run_to_rel_pos(self, address):
        side = self._get_motor_side(address)

        self.job_creator.create_single_job_left(
            self.dict['speed_' + side],
            self.dict['distance_' + side])

    def run_to_abs_pos_dual(self):
        velocity_max = max(self.dict['speed_left'], self.dict['speed_right'])

        self.job_creator.create_dual_job(velocity_max,
                                         self.dict['distance_left'],
                                         self.dict['distance_right'])
