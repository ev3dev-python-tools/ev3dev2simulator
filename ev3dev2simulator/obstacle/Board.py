from arcade import PointList, Color, arcade, Shape


class Board:
    """
    This class represents a 'rock'. Rocks are rectangles.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: arcade.Color):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0

        # visualisation
        self.color = color
        self.points = None
        self.shape = None

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, scale):
        self.points = self._create_points(scale)
        self.shape = self._create_shape()

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this rock in 2D space.
        :return: a PointList object.
        """
        return arcade.get_rectangle_points(self.x * scale,
                                           self.y * scale,
                                           self.width * scale,
                                           self.height * scale,
                                           self.angle)

    def _create_shape(self) -> Shape:
        """
        Create a shape representing the rectangle of this rock.
        :return: a Arcade shape object.
        """

        colors = []

        for i in range(4):
            colors.append(self.color)

        return arcade.create_rectangles_filled_with_colors(self.points, colors)
