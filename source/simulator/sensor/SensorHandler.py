class SensorHandler:
    """
    The MotorConnector class provides a translation layer between the raw motor classes
    and the motors on the actual robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the JobCreator to create movement jobs for
    the simulator.
    """


    def __init__(self):
        self.color_center = None
        self.color_left = None
        self.color_right = None


sensor_handler = SensorHandler()


def get_sensor_handler():
    return sensor_handler
