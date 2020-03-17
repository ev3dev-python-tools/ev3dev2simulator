import arcade
from arcade import Shape, PointList
from pymunk import Body, Poly, Vec2d

from ev3dev2simulator.obstacle.TouchObstacle import TouchObstacle


class Rock(TouchObstacle):
    """
    This class represents a 'rock'. Rocks are rectangles.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: arcade.Color,
                 angle: int):
        super(Rock, self).__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

        # visualisation
        self.color = color
        self.points = None
        self.shape = None
        self.poly = None

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, scale):
        self.points = self._create_points(scale)
        self.shape = self._create_shape()
        self.poly = self._create_poly(scale)

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        width = config['width']
        height = config['height']
        color = eval(config['color'])
        angle = config['angle']

        return cls(x, y, width, height, color, angle)

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

        top = arcade.create_rectangles_filled_with_colors(self.points, colors)

        return top

    def _create_poly(self, scale):
        """
        Create the polygon used for ray-casting. (Ultrasonic sensor)
        :return: a Pymunk Poly object.
        """

        body = Body(body_type=Body.STATIC)
        body.position = Vec2d(self.x * scale, self.y * scale)

        return Poly.create_box(body, (self.width * scale, self.height * scale))
