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


    def set_time(self, address: str, time: int):
        """
        Set the time to run of the motor belonging to the given address.
        :param address: of the motor
        :param time: in milliseconds.
        """

        self.dict['time_' + self._get_motor_side(address)] = time


    def set_speed(self, address: str, speed: float):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param address: of the motor
        :param speed: in degrees per second.
        """

        self.dict['speed_' + self._get_motor_side(address)] = speed


    def set_distance(self, address: str, distance: float):
        """
        Set the distance to run of the motor belonging to the given address.
        :param address: of the motor
        :param distance: in degrees.
        """

        self.dict['distance_' + self._get_motor_side(address)] = distance


    def set_stop_action(self, address: str, action: str):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param address: of the motor.
        :param action: stop action of the motor, this can be 'hold' or 'coast'.
        """

        self.dict['stop_action_' + self._get_motor_side(address)] = action


    def run_forever(self, address: str) -> float:
        """
        Run the motor indefinitely. This is translated to 3600 seconds.
        :param address: of the motor to run forever.
        :return an floating point value representing the number of seconds
        the given run operation will take. Here a large number is returned.
        In the real world this would be infinity.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        distance = speed * FOREVER_MOCK_SECONDS

        self._run(side, speed, distance)
        return 100000


    def run_to_rel_pos(self, address: str) -> float:
        """
        Run the motor for the distance needed to reach a certain position.
        :param address: of the motor to run.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        distance = self.dict['distance_' + side]

        return self._run(side, speed, distance)


    def run_timed(self, address: str) -> float:
        """
        Run the motor for a number of milliseconds.
        :param address: of the motor to run for a number of milliseconds.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        side = self._get_motor_side(address)

        speed = self.dict['speed_' + side]
        time = self.dict['time_' + side]
        distance = speed * (time / 1000)

        return self._run(side, speed, distance)


    def _run(self, side: str, speed: float, distance: float) -> float:
        """
        Run the motor at a speed for a distance.
        :param side: location of the motor, 'left', 'right' or 'center'.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        if speed == 0 or distance == 0:
            return 0

        stop_action = self.dict['stop_action_' + side]
        return self.job_creator.create_jobs(speed, distance, stop_action, side)


    def stop(self, address: str):

        side = self._get_motor_side(address)
        stop_action = self.dict['stop_action_' + side]

        self.job_creator.stop_jobs(stop_action, side)


    def _get_motor_side(self, address: str) -> str:
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
