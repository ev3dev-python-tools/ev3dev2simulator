"""
The border_obstacle module contains the class BorderObstacle
It is a class representing any obstacle acting as a square border.
"""

import arcade as _arcade

from ev3dev2simulator.obstacle.color_obstacle import ColorObstacle


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

        screen_height = self.rectangle_height * scale
        screen_width = self.rectangle_width * scale

        draw_depth = self.depth * scale

        screen_edge_spacing = self.edge_spacing * scale

        border_long_width = screen_width - screen_edge_spacing * 2
        border_long_height = screen_height - screen_edge_spacing * 2

        self.top_points = _arcade.get_rectangle_points(screen_center_x,
                                                       screen_height - screen_edge_spacing - (draw_depth / 2),
                                                       border_long_width,
                                                       draw_depth)

        self.right_points = _arcade.get_rectangle_points(screen_width - screen_edge_spacing - (draw_depth / 2),
                                                         screen_center_y,
                                                         draw_depth,
                                                         border_long_height)

        self.bottom_points = _arcade.get_rectangle_points(screen_center_x,
                                                          screen_edge_spacing + (draw_depth / 2),
                                                          border_long_width,
                                                          draw_depth)

        self.left_points = _arcade.get_rectangle_points(screen_edge_spacing + (draw_depth / 2),
                                                        screen_center_y,
                                                        draw_depth,
                                                        border_long_height)

    def collided_with(self, x: float, y: float) -> bool:
        for side in [self.top_points, self.right_points, self.bottom_points, self.left_points]:
            if _arcade.is_point_in_polygon(x, y, side):
                return True
        return False
