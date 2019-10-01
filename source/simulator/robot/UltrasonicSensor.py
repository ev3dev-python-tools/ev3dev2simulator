import math

from arcade import Point
from pymunk import Space, ShapeFilter

from simulator.util.Util import distance_between_points
from source.simulator.robot.Body import Body
from source.simulator.robot.ExtraBodyPart import ExtraBodyPart

SENSOR_HALF_HEIGHT = 15


class UltrasonicSensor(ExtraBodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int):
        super(UltrasonicSensor, self).__init__(address,
                                               img_cfg['ultrasonic_sensor'],
                                               0.13,
                                               body,
                                               delta_x,
                                               delta_y)


    def distance(self, space: Space) -> float:
        """
        Get the distance in pixels between this ultrasonic sensor and an object it is pointed to.
        If this sensor is not pointing towards an object return -1.
        :param space: which holds the visible objects.
        :return: a floating point value representing the distance.
        """

        x, y = self._calc_ray_cast_point()

        query = space.segment_query_first((self.center_x, self.center_y), (x, y), 1, ShapeFilter())
        if query:
            return -SENSOR_HALF_HEIGHT + distance_between_points(self.center_x,
                                                                 self.center_y,
                                                                 query.point.x,
                                                                 query.point.y)
        else:
            return -1


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
