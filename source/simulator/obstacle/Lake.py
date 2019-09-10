import arcade
from arcade import Shape

from source.simulator.util.Util import get_circle_points


class Lake:
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def __init__(self,
                 center_x: int,
                 center_y: int,
                 radius: float,
                 color: arcade.Color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

    def create(self) -> Shape:
        points = get_circle_points(self.center_x,
                                   self.center_y,
                                   self.radius)

        return arcade.create_line_strip(points, self.color, 15)
