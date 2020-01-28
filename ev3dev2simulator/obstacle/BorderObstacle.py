import arcade

from ev3dev2simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2simulator.util.Util import apply_scaling


class BorderObstacle(ColorObstacle):
    """
    This class provides basic functionality for obstacles which act as a border.
    """


    def __init__(self, cfg, color_code: int, depth: int, edge_spacing: float):
        super(BorderObstacle, self).__init__(color_code)

        self.screen_width = apply_scaling(cfg['screen_settings']['screen_width'])
        self.screen_height = apply_scaling(cfg['screen_settings']['screen_height'])
        self.depth = depth
        self.edge_spacing = edge_spacing

        self.top_points = None
        self.right_points = None
        self.bottom_points = None
        self.left_points = None

        self._calc_points()


    def _calc_points(self):
        """
        Calculate the points of the polygon this BorderObstacle consist of.
        """

        screen_center_x = self.screen_width / 2
        screen_center_y = self.screen_height / 2

        border_long_width = self.screen_width - self.edge_spacing * 2
        border_long_height = self.screen_height - self.edge_spacing * 2

        self.top_points = arcade.get_rectangle_points(screen_center_x,
                                                      self.screen_height - self.edge_spacing - (self.depth / 2),
                                                      border_long_width,
                                                      self.depth)

        self.right_points = arcade.get_rectangle_points(self.screen_width - self.edge_spacing - (self.depth / 2),
                                                        screen_center_y,
                                                        self.depth,
                                                        border_long_height)

        self.bottom_points = arcade.get_rectangle_points(screen_center_x,
                                                         self.edge_spacing + (self.depth / 2),
                                                         border_long_width,
                                                         self.depth)

        self.left_points = arcade.get_rectangle_points(self.edge_spacing + (self.depth / 2),
                                                       screen_center_y,
                                                       self.depth,
                                                       border_long_height)


    def collided_with(self, x: float, y: float) -> bool:
        if arcade.is_point_in_polygon(x, y, self.top_points):
            return True

        if arcade.is_point_in_polygon(x, y, self.left_points):
            return True

        if arcade.is_point_in_polygon(x, y, self.bottom_points):
            return True

        if arcade.is_point_in_polygon(x, y, self.right_points):
            return True

        return False
