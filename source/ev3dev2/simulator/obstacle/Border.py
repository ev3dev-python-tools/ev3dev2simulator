import arcade

from ev3dev2.simulator.obstacle.BorderObstacle import BorderObstacle
from ev3dev2.simulator.util.Util import apply_scaling


class Border(BorderObstacle):
    """
    The outer line surrounding the playing field.
    """


    def __init__(self, cfg, color: arcade.Color):
        depth = apply_scaling(cfg['obstacle_settings']['border_settings']['border_depth'])
        edge_spacing = apply_scaling(cfg['screen_settings']['edge_spacing'])

        super(Border, self).__init__(cfg, 6, depth, edge_spacing)

        self.color = color
        self.shapes = self._create_shapes()


    def _create_shapes(self) -> [arcade.Shape]:
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

        return [top, right, bottom, left]
