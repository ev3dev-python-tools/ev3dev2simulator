from ev3dev2.util.Singleton import Singleton
from simulator.job.JobCreator import JobCreator
from simulator.util.Util import load_config

FOREVER_MOCK_SECONDS = 3600


class MotorConnector(metaclass=Singleton):
    """
    The MotorConnector class provides a translation layer between the raw motor classes
    and the motors on the actual robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the JobCreator to create movement jobs for
    the simulator.
    """


    def __init__(self, job_handler):
        cfg = load_config()
        self.address_motor_center = cfg['motor_alloc_settings']['center_motor']
        self.address_motor_left = cfg['motor_alloc_settings']['left_motor']
        self.address_motor_right = cfg['motor_alloc_settings']['right_motor']

        self.dict = {}
        self.job_creator = JobCreator(job_handler)


    def set_time(self, address, time):
        """
        Set the time to run of the motor belonging to the given address.
        :param address: of the motor
        :param time: in milliseconds.
        """

        self.dict['time_' + self._get_motor_side(address)] = time


    def set_speed(self, address, speed):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param address: of the motor
        :param speed: in degrees per second.
        """

        self.dict['speed_' + self._get_motor_side(address)] = speed


    def set_distance(self, address, distance):
        """
        Set the distance to run of the motor belonging to the given address.
        :param address: of the motor
        :param distance: in degrees.
        """

        self.dict['distance_' + self._get_motor_side(address)] = distance


    def run_forever(self, address):
        """
        Run the motor indefinitely. This is translated to 3600 seconds.
        :param address: of the motor to run forever.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        distance = speed * FOREVER_MOCK_SECONDS

        if side == 'left':
            self.job_creator.create_jobs_left(speed, distance)
        else:
            self.job_creator.create_jobs_right(speed, distance)


    def run_to_rel_pos(self, address):
        """
        Run the motor for the distance needed to reach a certain position.
        :param address: of the motor to run.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        distance = self.dict['distance_' + side]

        if side == 'left':
            self.job_creator.create_jobs_left(speed, distance)
        else:
            self.job_creator.create_jobs_right(speed, distance)


    def run_timed(self, address):
        """
        Run the motor for a number of milliseconds.
        :param address: of the motor to run for a number of milliseconds.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        time = self.dict['time_' + side]
        distance = speed * (time / 1000)

        if side == 'left':
            self.job_creator.create_jobs_left(speed, distance)
        else:
            self.job_creator.create_jobs_right(speed, distance)


    def _get_motor_side(self, address) -> str:
        """
        Get the location of the motor on the actual robot based on its address.
        :param address: of the motor
        :return 'left', 'right' or 'center'
        """

        if self.address_motor_left == address:
            return 'left'

        if self.address_motor_right == address:
            return 'right'

        if self.address_motor_center == address:
            return 'center'
