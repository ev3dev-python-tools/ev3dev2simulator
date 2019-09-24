import arcade
from arcade import Shape

from simulator.obstacle.Obstacle import Obstacle
from simulator.util.Color import RED, GREEN, BLUE, to_color_code
from source.simulator.util.Util import get_circle_points


class Lake(Obstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """


    def __init__(self,
                 center_x: int,
                 center_y: int,
                 radius: float,
                 color: arcade.Color,
                 border_width: int):
        super(Lake, self).__init__(to_color_code(color))

        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color
        self.border_width = border_width


    def create(self) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """

        self.points = get_circle_points(self.center_x,
                                        self.center_y,
                                        self.radius)

        return arcade.create_line_strip(self.points,
                                        self.color,
                                        self.border_width)


class BlueLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = lake_cfg['border_width']
        inner_radius = lake_cfg['inner_radius']
        radius = inner_radius + (border_width / 2)

        edge_spacing = cfg['screen_settings']['edge_spacing']
        border_depth = cfg['obstacle_settings']['border_settings']['border_depth']

        x = lake_cfg['lake_blue_x'] + edge_spacing + border_depth
        y = lake_cfg['lake_blue_y'] + edge_spacing + border_depth

        super(BlueLake, self).__init__(x, y, radius, BLUE, border_width)


class GreenLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = lake_cfg['border_width']
        inner_radius = lake_cfg['inner_radius']
        radius = inner_radius + (border_width / 2)

        edge_spacing = cfg['screen_settings']['edge_spacing']
        border_depth = cfg['obstacle_settings']['border_settings']['border_depth']

        x = lake_cfg['lake_green_x'] + edge_spacing + border_depth
        y = lake_cfg['lake_green_y'] + edge_spacing + border_depth

        super(GreenLake, self).__init__(x, y, radius, GREEN, border_width)


class RedLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = lake_cfg['border_width']
        inner_radius = lake_cfg['inner_radius']
        radius = inner_radius + (border_width / 2)

        edge_spacing = cfg['screen_settings']['edge_spacing']
        border_depth = cfg['obstacle_settings']['border_settings']['border_depth']

        x = lake_cfg['lake_red_x'] + edge_spacing + border_depth
        y = lake_cfg['lake_red_y'] + edge_spacing + border_depth

        super(RedLake, self).__init__(x, y, radius, RED, border_width)
