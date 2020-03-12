import arcade
from arcade import Shape, PointList

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2simulator.obstacle.Hole import Hole
from ev3dev2simulator.util.Util import apply_scaling, get_circle_points, distance_between_points, to_color_code


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

        self.large_sim_type = get_config().is_large_sim_type()

        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.border_width = border_width

        self.radius = radius if self.large_sim_type else radius * 1.2
        self.inner_radius = inner_radius
        self.outer_radius = self.radius + (self.border_width / 2)

        self.points = self._create_points()
        self.shape = self._create_shape()

        self.hole = self._create_hole()

    @classmethod
    def from_config(cls, config):

        vis_conf = get_config().get_visualisation_config()

        border_width = apply_scaling(config['border_width'])
        inner_radius = apply_scaling(config['inner_radius'])
        radius = inner_radius + (border_width / 2)

        edge_spacing = apply_scaling(vis_conf['screen_settings']['edge_spacing'])
        border_depth = apply_scaling(sim_conf['obstacles']['border']['depth'])

        x = apply_scaling(config['x']) + edge_spacing + border_depth
        y = apply_scaling(config['y']) + edge_spacing + border_depth

        color = eval(config['color'])

        return cls(x, y, radius, inner_radius, color, border_width)

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

        if self.large_sim_type:
            return arcade.create_line_strip(self.points,
                                            self.color,
                                            self.border_width)
        else:
            color_list = [self.color] + [self.color] * (32 + 1)
            return arcade.create_line_generic_with_colors(self.points, color_list, 6)

    def _create_hole(self):
        return Hole(self.center_x, self.center_y, self.inner_radius)

    def collided_with(self, x: float, y: float) -> bool:
        distance = distance_between_points(self.center_x,
                                           self.center_y,
                                           x,
                                           y)

        if self.large_sim_type:
            return self.inner_radius < distance < self.outer_radius
        else:
            return distance < self.outer_radius
