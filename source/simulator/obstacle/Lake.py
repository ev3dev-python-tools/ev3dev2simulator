import arcade
from arcade import Shape

from simulator.util.Color import RED, GREEN, BLUE
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
                 color: arcade.Color,
                 border_width: int):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color
        self.border_width = border_width

    def create(self) -> Shape:
        points = get_circle_points(self.center_x,
                                   self.center_y,
                                   self.radius,
                                   48)

        return arcade.create_line_strip(points, self.color, self.border_width)


class RedLake(Lake):
    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        inner_radius = lake_cfg['inner_radius']
        border_width = lake_cfg['border_width']
        edge_spacing = cfg['screen_settings']['edge_spacing']

        x = lake_cfg['lake_red_x'] + inner_radius + (border_width / 2) + edge_spacing
        y = lake_cfg['lake_red_y'] + inner_radius + (border_width / 2) + edge_spacing

        super().__init__(x, y, inner_radius, RED, border_width)


class GreenLake(Lake):
    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        inner_radius = lake_cfg['inner_radius']
        border_width = lake_cfg['border_width']
        edge_spacing = cfg['screen_settings']['edge_spacing']

        x = lake_cfg['lake_green_x'] + inner_radius + (border_width / 2) + edge_spacing
        y = lake_cfg['lake_green_y'] + inner_radius + (border_width / 2) + edge_spacing

        super().__init__(x, y, inner_radius, GREEN, border_width)


class BlueLake(Lake):
    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        inner_radius = lake_cfg['inner_radius']
        border_width = lake_cfg['border_width']
        edge_spacing = cfg['screen_settings']['edge_spacing']

        x = lake_cfg['lake_blue_x'] + inner_radius + (border_width / 2) + edge_spacing
        y = lake_cfg['lake_blue_y'] + inner_radius + (border_width / 2) + edge_spacing

        super().__init__(x, y, inner_radius, BLUE, border_width)
