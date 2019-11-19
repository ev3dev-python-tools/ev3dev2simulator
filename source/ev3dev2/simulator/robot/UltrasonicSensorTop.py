import math

from arcade import Point
from pymunk import Space, ShapeFilter

from ev3dev2.simulator.config.config import get_config
from ev3dev2.simulator.robot import Robot
from ev3dev2.simulator.robot.BodyPart import BodyPart
from ev3dev2.simulator.util.Util import apply_scaling, distance_between_points


class UltrasonicSensor(BodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(UltrasonicSensor, self).__init__(address, robot, delta_x, delta_y)
        self.init_texture(img_cfg['ultrasonic_sensor_top'], 0.20)

        self.sensor_half_height = apply_scaling(22.5)
        self.scaling_multiplier = get_config().get_scale()


    def distance(self, space: Space) -> float:
        """
        Get the distance in pixels between this ultrasonic sensor and an object it is pointed to.
        If this sensor is not pointing towards an object return 2550, which is the max distance of the real robot's ultrasonic sensor.
        :param space: which holds the visible objects.
        :return: a floating point value representing the distance.
        """

        x, y = self._calc_ray_cast_point()

        query = space.segment_query_first((self.center_x, self.center_y), (x, y), 1, ShapeFilter())
        if query:
            return -self.sensor_half_height + distance_between_points(self.center_x,
                                                                      self.center_y,
                                                                      query.point.x,
                                                                      query.point.y)
        else:
            return self.get_default_value()


    def _calc_ray_cast_point(self) -> Point:
        """
        Calculate the coordinates of the point to perform a ray-cast towards
        which covers the entire playing field of the simulator.
        :return: a Point object representing the coordinates of the ray-cast point.
        """

        rad = math.radians(self.angle)

        x = 1000 * math.sin(-rad) + self.center_x
        y = 1000 * math.cos(-rad) + self.center_y

        return x, y


    def get_default_value(self):
        """
        1 pixel == 1mm so measurement values this sensor returns are one to one mappable to millimeters.
        Max distance real world robot ultrasonic sensor returns is 2550mm.
        :return: default value in pixels.
        """

        return 2550 * self.scaling_multiplier
