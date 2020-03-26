import math

from arcade import Point, create_line
from arcade.color import RED
from pymunk import Space, ShapeFilter

from ev3dev2simulator.config.config import get_simulation_settings, debug
from ev3dev2simulator.robot.BodyPart import BodyPart
from ev3dev2simulator.util.Util import distance_between_points


class UltrasonicSensor(BodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot.
    """
    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 delta_x: int,
                 delta_y: int,
                 name: str):
        dims = get_simulation_settings()['body_part_sizes']['ultrasonic_sensor_top']
        super(UltrasonicSensor, self).__init__(brick, address, robot, delta_x, delta_y,
                                               dims['width'], dims['height'], 'ultrasonic_sensor')
        self.name = name
        self.sensor_half_height = 22.5

    def setup_visuals(self, scale):
        img_cfg = get_simulation_settings()['image_paths']
        self.init_texture(img_cfg['ultrasonic_sensor_top'], scale)

    def get_latest_value(self):
        return self.distance(self.robot.space)

    def distance(self, space: Space) -> float:
        """
        Get the distance in pixels between this ultrasonic sensors eyes and an object it is pointed to.
        First check the left eye, if this does not see anything check the right eye.
        If this sensor is not pointing towards an object return 2550, which is the max distance of the real robot's ultrasonic sensor.
        :param space: which holds the visible objects.
        :return: a floating point value representing the distance.
        """
        left_eye_x, left_eye_y = self._calc_eye_center(self.angle + 90)
        distance = self._calc_view_distance(space, left_eye_x, left_eye_y)

        if distance:
            return distance * 1 / self.px_mm_scale

        right_eye_x, right_eye_y = self._calc_eye_center(self.angle - 90)
        distance = self._calc_view_distance(space, right_eye_x, right_eye_y)

        if distance:
            return distance * 1 / self.px_mm_scale

        return self.get_default_value()

    def _calc_view_distance(self, space: Space, base_x: float, base_y: float) -> float:
        """
        Calculate the distance between the base point, represented by base_x and base_y, and the furthest
        viewable object. If no object is in sight, return None.
        :param space: which holds the visible objects.
        :param base_x: x coordinate of the base point.
        :param base_y: y coordinate of the base point.
        :return: a floating point value representing the distance if object is viewable, else None.
        """
        x, y = self._calc_ray_cast_point(base_x, base_y)
        if debug:
            line = create_line(x, y, base_x, base_y, RED, 5)
            self.robot.debug_shapes.append(line)

        query = space.segment_query_first((base_x, base_y), (x, y), 1, ShapeFilter())
        if query:
            return -self.sensor_half_height + distance_between_points(base_x,
                                                                      base_y,
                                                                      query.point.x,
                                                                      query.point.y)
        else:
            return None

    def _calc_ray_cast_point(self, from_x: float, from_y: float) -> Point:
        """
        Calculate the coordinates of the point to perform a ray-cast towards
        which covers the entire playing field of the simulator.
        :return: a Point object representing the coordinates of the ray-cast point.
        """
        rad = math.radians(self.angle)

        x = 1000 * math.sin(-rad) + from_x
        y = 1000 * math.cos(-rad) + from_y

        return x, y

    def _calc_eye_center(self, angle: float) -> Point:
        """
        Calculate the center point of a location at the given angle relative to this objects center.
        :param angle: at which the new point is relative to this objects center.
        :return: a Point object representing the coordinates of the new location.
        """
        rad = math.radians(angle)
        eye_offset = 18
        x = eye_offset * math.sin(-rad) + self.center_x
        y = eye_offset * math.cos(-rad) + self.center_y

        return x, y

    def get_default_value(self):
        """
        1 pixel == 1mm so measurement values this sensor returns are one to one mappable to millimeters.
        Max distance real world robot ultrasonic sensor returns is 2550mm.
        :return: default value in pixels.
        """
        return 2550
