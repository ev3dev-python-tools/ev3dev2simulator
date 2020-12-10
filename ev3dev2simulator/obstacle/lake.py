"""
Module lake containing the class Lake, an obstacle on the playground.
"""

import arcade
from arcade import Shape, PointList, create_line_strip, create_ellipse_filled

from ev3dev2simulator.obstacle.color_obstacle import ColorObstacle
from ev3dev2simulator.obstacle.hole import Hole
from ev3dev2simulator.util.point import Point
from ev3dev2simulator.util.util import get_circle_points, distance_between_points, to_color_code


class Lake(ColorObstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """

    def __init__(self,
                 pos: Point,
                 outer_radius: float,
                 inner_radius: float,
                 color: arcade.Color,
                 border_width: int,
                 hole_config: (bool, int)
                 ):
        super(Lake, self).__init__(to_color_code(color))

        self.x = pos.x
        self.y = pos.y
        self.border_width = border_width

        self.inner_radius = inner_radius
        self.hole = None
        has_hole = hole_config[0]
        if has_hole:
            hole_depth = hole_config[1]
            self.hole = self._create_hole(hole_depth)
        self.outer_radius = outer_radius

        # visualisation
        self.center_x = None
        self.center_y = None
        self.color = color
        self.shape = None
        self.scale = None

    def get_shapes(self):
        """
        Returns the lake shape.
        """
        return [self.shape]

    def create_shape(self, scale):
        """
        Creates the shape of lake.
        """
        self.scale = scale
        self.center_x = self.x * scale
        self.center_y = self.y * scale
        self.shape = self._create_shape(scale)
        if self.hole is not None:
            self.hole.create_shape(scale)

    @classmethod
    def from_config(cls, config):
        """
        Creates a lakes based on the given config.
        """
        border_width = config['border_width']
        inner_radius = config['inner_radius']
        outer_radius = inner_radius + border_width

        pos = Point(config['x'], config['y'])
        has_hole = config['hole'] if 'hole' in config else True
        depth = config['depth'] if 'depth' in config else 800

        color = tuple(config['color'])

        return cls(pos, outer_radius, inner_radius, color, border_width, (has_hole, depth))

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.outer_radius * scale)

    def _create_shape(self, scale) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """
        if self.hole is not None:
            points = self._create_points(scale)
            return create_line_strip(points,
                                     self.color,
                                     self.border_width * scale)
        return create_ellipse_filled(self.center_x, self.center_y,
                                     self.outer_radius * scale, self.outer_radius * scale, self.color)

    def _create_hole(self, depth):
        """
        Create hole object in lake that is used for detection that the robot is stuck.
        """
        return Hole(self.x, self.y, self.inner_radius, depth)

    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if the lake overlaps with a robot.
        """
        distance = distance_between_points(self.center_x, self.center_y, x, y)
        if self.hole is not None:
            return (self.inner_radius * self.scale) < distance <\
                   ((self.outer_radius + (self.border_width/2)) * self.scale)
        return distance < (self.outer_radius * self.scale)
