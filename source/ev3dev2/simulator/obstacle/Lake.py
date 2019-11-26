import arcade
from arcade import Shape, PointList

from ev3dev2.simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2.simulator.obstacle.Hole import Hole
from ev3dev2.simulator.util.Color import to_color_code, BLUE, RED, GREEN
from ev3dev2.simulator.util.Util import apply_scaling, get_circle_points, distance_between_points


class Lake(ColorObstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """


    def __init__(self,
                 center_x: int,
                 center_y: int,
                 radius: float,
                 inner_radius: float,
                 color: arcade.Color,
                 border_width: int):
        super(Lake, self).__init__(to_color_code(color))

        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.border_width = border_width

        self.radius = radius
        self.inner_radius = inner_radius
        self.outer_radius = self.radius + (self.border_width / 2)

        self.points = self._create_points()
        self.shape = self._create_shape()

        self.hole = self._create_hole()


    def _create_points(self) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.radius)


    def _create_shape(self) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """

        return arcade.create_line_strip(self.points,
                                        self.color,
                                        self.border_width)


    def _create_hole(self):
        return Hole(self.center_x, self.center_y, self.inner_radius)


    def collided_with(self, x: float, y: float) -> bool:
        distance = distance_between_points(self.center_x,
                                           self.center_y,
                                           x,
                                           y)

        return self.inner_radius < distance < self.outer_radius


class BlueLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = apply_scaling(lake_cfg['border_width'])
        inner_radius = apply_scaling(lake_cfg['inner_radius'])
        radius = inner_radius + (border_width / 2)

        edge_spacing = apply_scaling(cfg['screen_settings']['edge_spacing'])
        border_depth = apply_scaling(cfg['obstacle_settings']['border_settings']['border_depth'])

        x = apply_scaling(lake_cfg['lake_blue_x']) + edge_spacing + border_depth
        y = apply_scaling(lake_cfg['lake_blue_y']) + edge_spacing + border_depth

        super(BlueLake, self).__init__(x, y, radius, inner_radius, BLUE, border_width)


class GreenLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = apply_scaling(lake_cfg['border_width'])
        inner_radius = apply_scaling(lake_cfg['inner_radius'])
        radius = inner_radius + (border_width / 2)

        edge_spacing = apply_scaling(cfg['screen_settings']['edge_spacing'])
        border_depth = apply_scaling(cfg['obstacle_settings']['border_settings']['border_depth'])

        x = apply_scaling(lake_cfg['lake_green_x']) + edge_spacing + border_depth
        y = apply_scaling(lake_cfg['lake_green_y']) + edge_spacing + border_depth

        super(GreenLake, self).__init__(x, y, radius, inner_radius, GREEN, border_width)


class RedLake(Lake):

    def __init__(self, cfg):
        lake_cfg = cfg['obstacle_settings']['lake_settings']

        border_width = apply_scaling(lake_cfg['border_width'])
        inner_radius = apply_scaling(lake_cfg['inner_radius'])
        radius = inner_radius + (border_width / 2)

        edge_spacing = apply_scaling(cfg['screen_settings']['edge_spacing'])
        border_depth = apply_scaling(cfg['obstacle_settings']['border_settings']['border_depth'])

        x = apply_scaling(lake_cfg['lake_red_x']) + edge_spacing + border_depth
        y = apply_scaling(lake_cfg['lake_red_y']) + edge_spacing + border_depth

        super(RedLake, self).__init__(x, y, radius, inner_radius, RED, border_width)
