import arcade

from ev3dev2simulator.obstacle.ColorObstacle import ColorObstacle


class BorderObstacle(ColorObstacle):
    """
    This class provides basic functionality for obstacles which act as a border.
    """

    def __init__(self, rectangle_width, rectangle_height, color_code: int, depth: int, edge_spacing: float):
        super(BorderObstacle, self).__init__(color_code)

        self.rectangle_width = rectangle_width
        self.rectangle_height = rectangle_height
        self.depth = depth
        self.edge_spacing = edge_spacing

        self.top_points = None
        self.right_points = None
        self.bottom_points = None
        self.left_points = None

    def _calc_points(self, scale):
        """
        Calculate the points of the polygon this BorderObstacle consist of.
        """

        screen_center_x = (self.rectangle_width / 2) * scale
        screen_center_y = (self.rectangle_height / 2) * scale

        height_min_spacing = (self.rectangle_height - self.edge_spacing) * scale
        width_min_spacing = (self.rectangle_width - self.edge_spacing) * scale
        draw_depth = self.depth * scale
        border_long_width = (self.rectangle_width - self.edge_spacing * 2) * scale
        border_long_height = (self.rectangle_height - self.edge_spacing * 2) * scale

        self.top_points = arcade.get_rectangle_points(screen_center_x,
                                                      height_min_spacing - (draw_depth / 2),
                                                      border_long_width,
                                                      draw_depth)

        self.right_points = arcade.get_rectangle_points(width_min_spacing - (draw_depth / 2),
                                                        screen_center_y,
                                                        draw_depth,
                                                        border_long_height)

        self.bottom_points = arcade.get_rectangle_points(screen_center_x,
                                                         (self.edge_spacing * scale) + (draw_depth / 2),
                                                         border_long_width,
                                                         draw_depth)

        self.left_points = arcade.get_rectangle_points((self.edge_spacing * scale) + (draw_depth / 2),
                                                       screen_center_y,
                                                       draw_depth,
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
