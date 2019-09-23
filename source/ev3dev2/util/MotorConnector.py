from ev3dev2.util.MotorCommandCreator import MotorCommandCreator
from ev3dev2.util.Singleton import Singleton

FOREVER_MOCK_SECONDS = 3600


class MotorConnector(metaclass=Singleton):
    """
    The MotorConnector class provides a translation layer between the raw motor classes
    and the motors on the actual robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the MotorCommandCreator to create movement commands for
    the simulator.
    """


    def __init__(self):
        self.dict = {}
        self.job_creator = MotorCommandCreator()


    def set_time(self, address: str, time: int):
        """
        Set the time to run of the motor belonging to the given address.
        :param address: of the motor
        :param time: in milliseconds.
        """

        self.dict['time_' + address] = time


    def set_speed(self, address: str, speed: float):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param address: of the motor
        :param speed: in degrees per second.
        """

        self.dict['speed_' + address] = speed


    def set_distance(self, address: str, distance: float):
        """
        Set the distance to run of the motor belonging to the given address.
        :param address: of the motor
        :param distance: in degrees.
        """

        self.dict['distance_' + address] = distance


    def set_stop_action(self, address: str, action: str):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param address: of the motor.
        :param action: stop action of the motor, this can be 'hold' or 'coast'.
        """

        self.dict['stop_action_' + address] = action


    def run_forever(self, address: str) -> float:
        """
        Run the motor indefinitely. This is translated to 3600 seconds.
        :param address: of the motor to run forever.
        :return an floating point value representing the number of seconds
        the given run operation will take. Here a large number is returned.
        In the real world this would be infinity.
        """

        speed = self.dict['speed_' + address]
        distance = speed * FOREVER_MOCK_SECONDS

        self._run(address, speed, distance)
        return 100000


    def run_to_rel_pos(self, address: str) -> float:
        """
        Run the motor for the distance needed to reach a certain position.
        :param address: of the motor to run.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        speed = self.dict['speed_' + address]
        distance = self.dict['distance_' + address]

        return self._run(address, speed, distance)


    def run_timed(self, address: str) -> float:
        """
        Run the motor for a number of milliseconds.
        :param address: of the motor to run for a number of milliseconds.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        speed = self.dict['speed_' + address]
        time = self.dict['time_' + address]
        distance = speed * (time / 1000)

        return self._run(address, speed, distance)


    def _run(self, address: str, speed: float, distance: float) -> float:
        """
        Run the motor at a speed for a distance.
        :param address: of the motor to run.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        if speed == 0 or distance == 0:
            return 0

        stop_action = self.dict['stop_action_' + address]
        return self.job_creator.create_command(speed, distance, stop_action, address)


    def stop(self, address: str):
        pass
