import arcade
from arcade import Shape


class Rock:
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
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle


    def create(self) -> Shape:
        """
        Create a shape representing the inner rectangle of this rock.
        :return: a Arcade shape object.
        """

        return arcade.create_rectangle_filled(self.center_x,
                                              self.center_y,
                                              self.width,
                                              self.height,
                                              self.color,
                                              self.angle)


    def create_outline(self) -> Shape:
        """
        Create a shape representing the outline rectangle of this rock.
        :return: a Arcade shape object.
        """

        return arcade.create_rectangle_outline(self.center_x,
                                               self.center_y,
                                               self.width,
                                               self.height,
                                               arcade.color.BLACK,
                                               2,
                                               self.angle)
