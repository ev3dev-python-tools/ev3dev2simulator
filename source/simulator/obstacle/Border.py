import arcade
from arcade import Shape

from simulator.obstacle.Obstacle import Obstacle


class Border(Obstacle):
    """
    The outer line surrounding the playing field.
    """


    def __init__(self, cfg, color: arcade.Color):
        super(Border, self).__init__(6)

        self.screen_width = cfg['screen_settings']['screen_width']
        self.screen_height = cfg['screen_settings']['screen_height']
        self.depth = cfg['obstacle_settings']['border_settings']['border_depth']
        self.edge_spacing = cfg['screen_settings']['edge_spacing']
        self.color = color

        self.top_points = None
        self.right_points = None
        self.bottom_points = None
        self.left_points = None
        self.calc_points()


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


    def create(self) -> [Shape]:
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


    def collided_with(self, sprite: arcade.Sprite) -> bool:
        if arcade.are_polygons_intersecting(self.top_points, sprite.points):
            return True

        if arcade.are_polygons_intersecting(self.left_points, sprite.points):
            return True

        if arcade.are_polygons_intersecting(self.bottom_points, sprite.points):
            return True

        if arcade.are_polygons_intersecting(self.right_points, sprite.points):
            return True

        return False
