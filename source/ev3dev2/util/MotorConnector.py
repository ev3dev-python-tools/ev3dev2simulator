from ev3dev2.util.MotorCommandCreator import get_motor_command_creator

FOREVER_MOCK_SECONDS = 3600


class MotorConnector:
    """
    The MotorConnector class provides a translation layer between the ev3dev2 motor classes
    and the motors on the simulated robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the MotorCommandCreator to create movement commands for
    the simulator.
    """


    def __init__(self, address: str):
        self.address = address

        self.speed = None
        self.distance = None
        self.time = None
        self.stop_action = None

        self.job_creator = get_motor_command_creator()


    def set_time(self, time: int):
        """
        Set the time to run of the motor belonging to the given address.
        :param time: in milliseconds.
        """

        self.time = time


    def set_speed(self, speed: float):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param speed: in degrees per second.
        """

        self.speed = speed


    def set_distance(self, distance: float):
        """
        Set the distance to run of the motor belonging to the given address.
        :param distance: in degrees.
        """

        self.distance = distance


    def set_stop_action(self, action: str):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param action: stop action of the motor, this can be 'hold' or 'coast'.
        """

        self.stop_action = action


    def run_forever(self) -> float:
        """
        Run the motor indefinitely. This is translated to 3600 seconds.
        :return an floating point value representing the number of seconds
        the given run operation will take. Here a large number is returned.
        In the real world this would be infinity.
        """

        distance = self.speed * FOREVER_MOCK_SECONDS
        self._run(self.speed, distance)

        return 100000


    def run_to_rel_pos(self) -> float:
        """
        Run the motor for the distance needed to reach a certain position.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        return self._run(self.speed, self.distance)


    def run_timed(self) -> float:
        """
        Run the motor for a number of milliseconds.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        distance = self.speed * (self.time / 1000)
        return self._run(self.speed, distance)


    def _run(self, speed: float, distance: float) -> float:
        """
        Run the motor at a speed for a distance.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return an floating point value representing the number of seconds
        the given run operation will take.
        """

        if speed == 0 or distance == 0:
            return 0

        return self.job_creator.create_drive_command(speed,
                                                     distance,
                                                     self.stop_action,
                                                     self.address)


    def stop(self):
        speed = self.speed if self.speed else 0
        stop_action = self.stop_action if self.stop_action else 0
        distance = self.distance if self.distance else 0

        if speed == 0:
            return

        if distance < 0:
            speed *= -1

        self.job_creator.create_stop_command(speed, stop_action, self.address)
