"""
Module containing the class Hole, used to detect robots driving into lakes.
"""


import arcade
from arcade import PointList

from ev3dev2simulator.util.util import get_circle_points


class Hole:
    """
    This class represents a the 'hole' of a 'lake'.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 radius: float,
                 depth: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.depth = depth

        # visualisation
        self.points = None

    def create_shape(self, scale):
        """
        Creates the shape of the hole.
        """
        self.points = self._create_points(scale)

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.x * scale,
                                 self.y * scale,
                                 self.radius * scale)

    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if this obstacle has collided with the given Point. Meaning the point is inside this obstacle
        :param x: coordinate of the point.
        :param y: coordinate of the point.
        :return: True if collision detected.
        """

        return arcade.is_point_in_polygon(x, y, self.points)
