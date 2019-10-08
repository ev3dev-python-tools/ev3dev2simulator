import arcade
from arcade import Shape

from ev3dev2.simulator.obstacle.ColorObstacle import ColorObstacle
from ev3dev2.simulator.util.Util import apply_scaling


class Border(ColorObstacle):
    """
    The outer line surrounding the playing field.
    """


    def __init__(self, cfg, color: arcade.Color):
        super(Border, self).__init__(1)

        self.screen_width = apply_scaling(cfg['screen_settings']['screen_width'])
        self.screen_height = apply_scaling(cfg['screen_settings']['screen_height'])
        self.depth = apply_scaling(cfg['obstacle_settings']['border_settings']['border_depth'])
        self.edge_spacing = apply_scaling(cfg['screen_settings']['edge_spacing'])
        self.color = color

        self.top_points = None
        self.right_points = None
        self.bottom_points = None
        self.left_points = None

        self.calc_points()
        self.shapes = self._create_shapes()


    def calc_points(self):
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


    def _create_shapes(self) -> [Shape]:
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
