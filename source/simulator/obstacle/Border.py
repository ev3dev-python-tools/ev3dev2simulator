import arcade
from arcade import Shape


class Border:

    def __init__(self,
                 screen_width: int,
                 screen_height: int,
                 width: int,
                 border_spacing: int,
                 color: arcade.Color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = width
        self.border_spacing = border_spacing
        self.color = color

    def create(self) -> [Shape]:
        screen_center_x = self.screen_width / 2
        screen_center_y = self.screen_height / 2

        border_long_width = self.screen_width - self.border_spacing * 2 + self.width
        border_long_height = self.screen_height - self.border_spacing * 2 + self.width

        top = arcade.create_rectangle_filled(screen_center_x,
                                             self.screen_height - self.border_spacing,
                                             border_long_width,
                                             self.width,
                                             self.color)

        right = arcade.create_rectangle_filled(self.screen_width - self.border_spacing,
                                               screen_center_y,
                                               self.width,
                                               border_long_height,
                                               self.color)

        bottom = arcade.create_rectangle_filled(screen_center_x,
                                                self.border_spacing,
                                                border_long_width,
                                                self.width,
                                                self.color)

        left = arcade.create_rectangle_filled(self.border_spacing,
                                              screen_center_y,
                                              self.width,
                                              border_long_height,
                                              self.color)

        return [top, right, bottom, left]
