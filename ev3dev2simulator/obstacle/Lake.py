import arcade
from arcade import Shape, PointList

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2simulator.obstacle.Hole import Hole
from ev3dev2simulator.util.Util import get_circle_points, distance_between_points, to_color_code


class Lake(ColorObstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 radius: float,
                 inner_radius: float,
                 color: arcade.Color,
                 border_width: int):
        super(Lake, self).__init__(to_color_code(color))

        # TODO large sim type is gone, not sure what to do with this
        self.lake_type = True

        self.x = x
        self.y = y
        self.border_width = border_width

        self.radius = radius
        self.inner_radius = inner_radius
        self.outer_radius = self.radius + (self.border_width / 2)

        self.hole = self._create_hole()

        # visualisation
        self.color = color
        self.points = None
        self.shape = None

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, scale):
        self.points = self._create_points(scale)
        self.shape = self._create_shape(scale)
        self.hole.create_shape(scale)

    @classmethod
    def from_config(cls, config):

        vis_conf = get_config().get_visualisation_config()

        border_width = config['border_width']
        inner_radius = config['inner_radius']
        radius = inner_radius + (border_width / 2)

        edge_spacing = vis_conf['screen_settings']['edge_spacing']
        border_depth = vis_conf['screen_settings']['border_width']

        x = config['x'] + edge_spacing + border_depth
        y = config['y'] + edge_spacing + border_depth

        color = eval(config['color'])

        return cls(x, y, radius, inner_radius, color, border_width)

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.x * scale,
                                 self.y * scale,
                                 self.radius * scale)

    def _create_shape(self, scale) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """

        if self.lake_type:
            return arcade.create_line_strip(self.points,
                                            self.color,
                                            self.border_width * scale)
        else:
            color_list = [self.color] + [self.color] * (32 + 1)
            return arcade.create_line_generic_with_colors(self.points, color_list, 6)

    def _create_hole(self):
        return Hole(self.x, self.y, self.inner_radius)

    def collided_with(self, x: float, y: float) -> bool:
        distance = distance_between_points(self.x,
                                           self.y,
                                           x,
                                           y)

        if self.lake_type:
            return self.inner_radius < distance < self.outer_radius
        else:
            return distance < self.outer_radius
