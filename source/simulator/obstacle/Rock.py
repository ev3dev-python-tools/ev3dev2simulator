import arcade
from arcade import Shape

from simulator.obstacle.Obstacle import Obstacle


class Rock(Obstacle):
    """
    This class represents a 'rock'. Rocks consist of an inner rectangle
    with outer outline rectangle functioning as the border.
    """


    def __init__(self,
                 center_x: int,
                 center_y: int,
                 width: int,
                 height: int,
                 color: arcade.Color,
                 angle: int):
        super().__init__(1)

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle


    def create(self) -> Shape:
        """
        Create a shape representing the rectangle of this rock.
        :return: a Arcade shape object.
        """

        self.points = arcade.get_rectangle_points(self.center_x,
                                                  self.center_y,
                                                  self.width,
                                                  self.height,
                                                  self.angle)
        colors = []
        for i in range(4):
            colors.append(self.color)

        top = arcade.create_rectangles_filled_with_colors(self.points, colors)

        return top
