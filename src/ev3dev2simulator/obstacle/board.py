"""
The module board contains the class Board, the background of the playing field.
"""


import arcade as _arcade

from ev3dev2simulator.obstacle.color_obstacle import ColorObstacle
from ev3dev2simulator.util.util import to_color_code


class Board(ColorObstacle):
    """
    This class represents a 'Board'. The background of the playing field.
    """

    def __init__(self,
                 x: float,
                 y: float,
                 width: int,
                 height: int,
                 color: _arcade.Color):
        super(Board, self).__init__(to_color_code(color))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0

        # visualisation
        self.color = color
        self.points = None
        self.shape = None

    def get_shapes(self):
        """
        Returns the border shape.
        """
        return [self.shape]

    def create_shape(self, scale):
        """
        Creates the shape of the border.
        """
        self.points = self._create_points(scale)
        self.shape = self._create_shape()

    def _create_points(self, scale) -> _arcade.PointList:
        """
        Create a list of points representing this rock in 2D space.
        :return: a PointList object.
        """
        return _arcade.get_rectangle_points(self.x * scale,
                                            self.y * scale,
                                            self.width * scale,
                                            self.height * scale,
                                            self.angle)

    def _create_shape(self) -> _arcade.Shape:
        """
        Create a shape representing the rectangle of this rock.
        :return: a Arcade shape object.
        """

        colors = []

        for _ in range(4):
            colors.append(self.color)

        return _arcade.create_rectangles_filled_with_colors(self.points, colors)

    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if this obstacle has collided with the given Point. Meaning the point is inside this obstacle
        :param x: coordinate of the  point.
        :param y: coordinate of the point.
        :return: True if collision detected.
        """

        return _arcade.is_point_in_polygon(x, y, self.points)
