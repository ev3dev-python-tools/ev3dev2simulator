import arcade
from arcade import Shape


class Border:

    def __init__(self, cfg, color: arcade.Color):
        self.screen_width = cfg['screen_settings']['screen_width']
        self.screen_height = cfg['screen_settings']['screen_height']
        self.depth = cfg['obstacle_settings']['border_settings']['border_depth']
        self.border_spacing = cfg['screen_settings']['edge_spacing']
        self.color = color

    def create(self) -> [Shape]:
        screen_center_x = self.screen_width / 2
        screen_center_y = self.screen_height / 2

        border_long_width = self.screen_width - self.border_spacing * 2 + self.depth
        border_long_height = self.screen_height - self.border_spacing * 2 + self.depth

        top = arcade.create_rectangle_filled(screen_center_x,
                                             self.screen_height - self.border_spacing,
                                             border_long_width,
                                             self.depth,
                                             self.color)

        right = arcade.create_rectangle_filled(self.screen_width - self.border_spacing,
                                               screen_center_y,
                                               self.depth,
                                               border_long_height,
                                               self.color)

        bottom = arcade.create_rectangle_filled(screen_center_x,
                                                self.border_spacing,
                                                border_long_width,
                                                self.depth,
                                                self.color)

        left = arcade.create_rectangle_filled(self.border_spacing,
                                              screen_center_y,
                                              self.depth,
                                              border_long_height,
                                              self.color)

        return [top, right, bottom, left]
