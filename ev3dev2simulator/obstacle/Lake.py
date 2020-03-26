import arcade
from arcade import Shape, PointList, Color, create_line_generic, Point, get_points_for_thick_line, \
    create_triangles_filled_with_colors
from pyglet import gl
from typing import List

from ev3dev2simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2simulator.obstacle.Hole import Hole
from ev3dev2simulator.util.Util import get_circle_points, distance_between_points, to_color_code


# TODO remove this function if it is fixed in arcade
def create_line_strip(point_list: PointList,
                      color: Color, line_width: float = 1):
    """
    Create a multi-point line to be rendered later. This works faster than draw_line because
    the vertexes are only loaded to the graphics card once, rather than each frame.

    :param PointList point_list:
    :param Color color:
    :param PointList line_width:

    :Returns Shape:

    """
    if line_width == 1:
        return create_line_generic(point_list, color, gl.GL_LINE_STRIP, line_width)
    else:
        triangle_point_list: List[Point] = []
        new_color_list: List[Color] = []
        for i in range(1, len(point_list)):
            start_x = point_list[i - 1][0]
            start_y = point_list[i - 1][1]
            end_x = point_list[i][0]
            end_y = point_list[i][1]
            color1 = color
            color2 = color
            points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
            new_color_list += color1, color2, color1, color2
            triangle_point_list += points[1], points[0], points[2], points[3]

        shape = create_triangles_filled_with_colors(triangle_point_list, new_color_list)
        return shape


class Lake(ColorObstacle):
    """
    This class represents a 'lake'. Lakes consist of a transparent circle
    with a thick colored border.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 outer_radius: float,
                 inner_radius: float,
                 color: arcade.Color,
                 border_width: int,
                 has_hole: bool):
        super(Lake, self).__init__(to_color_code(color))

        self.x = x
        self.y = y
        self.border_width = border_width

        self.inner_radius = inner_radius
        self.hole = None
        if has_hole:
            self.hole = self._create_hole()
        self.outer_radius = outer_radius
        # visualisation
        self.center_x = None
        self.center_y = None
        self.color = color
        self.points = None
        self.shape = None
        self.scale = None

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, scale):
        self.scale = scale
        self.center_x = self.x * scale
        self.center_y = self.y * scale
        self.points = self._create_points(scale)
        self.shape = self._create_shape(scale)
        if self.hole is not None:
            self.hole.create_shape(scale)

    @classmethod
    def from_config(cls, config):

        border_width = config['border_width']
        inner_radius = config['inner_radius']
        outer_radius = inner_radius + border_width

        x = config['x']
        y = config['y']
        try:
            has_hole = bool(config['hole'])
        except:
            has_hole = True

        color = eval(config['color'])

        return cls(x, y, outer_radius, inner_radius, color, border_width, has_hole)

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this Lake in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.outer_radius * scale)

    def _create_shape(self, scale) -> Shape:
        """
        Create a shape representing this lake.
        :return: a Arcade shape object.
        """

        if self.hole is not None:
            return create_line_strip(self.points,
                                     self.color,
                                     self.border_width * scale)
        else:
            color_list = [self.color] + [self.color] * (32 + 1)
            return arcade.create_line_generic_with_colors(self.points, color_list, 6)

    def _create_hole(self):
        return Hole(self.x, self.y, self.inner_radius)

    def collided_with(self, x: float, y: float) -> bool:
        distance = distance_between_points(self.center_x,
                                           self.center_y,
                                           x,
                                           y)
        if self.hole is not None:
            return (self.inner_radius * self.scale) < distance <\
                   ((self.outer_radius + (self.border_width/2)) * self.scale)
        else:
            return distance < (self.outer_radius * self.scale)
