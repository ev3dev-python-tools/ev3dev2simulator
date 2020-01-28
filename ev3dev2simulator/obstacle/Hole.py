import arcade
from arcade import PointList

from ev3dev2simulator.util.Util import get_circle_points


class Hole:
    """
    This class represents a the 'hole' of a 'lake'.
    """


    def __init__(self,
                 center_x: int,
                 center_y: int,
                 radius: float):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

        self.points = self._create_points()


    def _create_points(self) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.radius)


    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if this obstacle has collided with the given Point. Meaning the point is inside this obstacle
        :param x: coordinate of the point.
        :param y: coordinate of the point.
        :return: True if collision detected.
        """

        return arcade.is_point_in_polygon(x, y, self.points)
