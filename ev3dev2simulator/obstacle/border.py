"""
The module border contains the class Border. A class representing the colored border around the playing field.
"""

import arcade as _arcade

from ev3dev2simulator.obstacle.border_obstacle import BorderObstacle
from ev3dev2simulator.util.util import to_color_code


class Border(BorderObstacle):
    """
    The outer line surrounding the playing field.
    """

    def __init__(self, board_width, board_height, color: _arcade.Color, depth, edge_spacing):
        super(Border, self).__init__(board_width, board_height, to_color_code(color), depth, edge_spacing)

        # visualisation
        self.color = color
        self.shapes = None

    def get_shapes(self):
        """
        Returns the border shape.
        """
        return self.shapes

    @classmethod
    def from_config(cls, board_width, board_height, config):
        """
        Create a border from config.
        """
        color = tuple(config['color'])
        depth = config['depth']
        spacing = config['outer_spacing']

        return cls(board_width, board_height, color, depth, spacing)

    def create_shape(self, scale) -> [_arcade.Shape]:
        """
        Create a list of shapes representing the four lines that make up this border.
        :return: a list of Arcade shapes.
        """
        self._calc_points(scale)
        colors = [self.color for _ in range(4)]
        self.shapes = []
        for side in [self.top_points, self.right_points, self.bottom_points, self.left_points]:
            self.shapes.append(_arcade.create_rectangles_filled_with_colors(side, colors))
        return self.shapes
