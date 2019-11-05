from ev3dev2.simulator.robot import Robot
from ev3dev2.simulator.robot.BodyPart import BodyPart
from ev3dev2.simulator.util.Util import apply_scaling


class UltrasonicSensorBottom(BodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot mounted towards the ground.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(UltrasonicSensorBottom, self).__init__(address,
                                                     img_cfg['ultrasonic_sensor_bottom'],
                                                     apply_scaling(0.20),
                                                     robot,
                                                     delta_x,
                                                     delta_y)


    def distance(self) -> float:
        """
        Get the distance in pixels between this ultrasonic sensor and an the ground.
        :return: a floating point value representing the distance.
        """

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return self.get_default_value()

        return 20


    def get_default_value(self):
        """
        1 pixel == 1mm so measurement values this sensor returns are one to one mappable to millimeters.
        Max distance real world robot ultrasonic sensor returns is 2550mm.
        :return: default value in pixels.
        """

        return 2550
