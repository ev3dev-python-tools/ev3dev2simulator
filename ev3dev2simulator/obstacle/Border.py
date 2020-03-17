import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.BorderObstacle import BorderObstacle
from ev3dev2simulator.util.Util import to_color_code


class Border(BorderObstacle):
    """
    The outer line surrounding the playing field.
    """

    def __init__(self, board_width, board_height, color: arcade.Color, depth):
        edge_spacing = get_config().get_visualisation_config()['screen_settings']['edge_spacing']

        super(Border, self).__init__(board_width, board_height, to_color_code(color), depth, edge_spacing)

        # visualisation
        self.color = color
        self.shapes = None

    def get_shapes(self):
        return self.shapes

    @classmethod
    def from_config(cls, board_width, board_height, config):

        color = eval(config['color'])
        depth = config['depth']

        return cls(board_width, board_height, color, depth)

    def create_shape(self, scale) -> [arcade.Shape]:

        self._calc_points(scale)
        """
        Create a list of shapes representing the four lines that make up this border.
        :return: a list of Arcade shapes.
        """

        colors = []
        for i in range(4):
            colors.append(self.color)

        top = arcade.create_rectangles_filled_with_colors(self.top_points, colors)
        right = arcade.create_rectangles_filled_with_colors(self.right_points, colors)
        bottom = arcade.create_rectangles_filled_with_colors(self.bottom_points, colors)
        left = arcade.create_rectangles_filled_with_colors(self.left_points, colors)

        self.shapes = [top, right, bottom, left]
