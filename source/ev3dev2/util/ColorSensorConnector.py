from ev3dev2.util.Singleton import Singleton
from simulator.util.Util import load_config


class ColorSensorConnector(metaclass=Singleton):
    """
    The MotorConnector class provides a translation layer between the raw motor classes
    and the motors on the actual robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the JobCreator to create movement jobs for
    the simulator.
    """


    def __init__(self, sensor_handler):
        cfg = load_config()
        self.address_motor_center = cfg['alloc_settings']['color_sensor']['center']
        self.address_motor_left = cfg['alloc_settings']['color_sensor']['left']
        self.address_motor_right = cfg['alloc_settings']['color_sensor']['right']

        self.sensor_handler = sensor_handler


    def get_color(self, address: str):
        """
        Set the time to run of the motor belonging to the given address.
        :param address: of the motor
        :param time: in milliseconds.
        """

        if self.address_motor_center == address:
            return self.sensor_handler.color_center

        if self.address_motor_left == address:
            return self.sensor_handler.color_left

        if self.address_motor_right == address:
            return self.sensor_handler.color_right

        return None
