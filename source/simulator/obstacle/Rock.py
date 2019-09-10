import arcade
from arcade import Shape


class Rock:

    def __init__(self,
                 center_x: int,
                 center_y: int,
                 width: int,
                 height: int,
                 color: arcade.Color,
                 angle: int):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle

    def create(self) -> Shape:
        return arcade.create_rectangle_filled(self.center_x,
                                              self.center_y,
                                              self.width,
                                              self.height,
                                              self.color,
                                              self.angle)

    def create_outline(self) -> Shape:
        return arcade.create_rectangle_outline(self.center_x,
                                               self.center_y,
                                               self.width,
                                               self.height,
                                               arcade.color.BLACK,
                                               2,
                                               self.angle)
