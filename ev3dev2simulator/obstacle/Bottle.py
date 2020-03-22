import arcade
from arcade import Shape, PointList
from pymunk import Body, Vec2d, Circle

from ev3dev2simulator.obstacle.TouchObstacle import TouchObstacle
from ev3dev2simulator.util.Util import get_circle_points


class Bottle(TouchObstacle):
    """
    This class represents a 'bottle'. Bottles are circles.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 radius: float,
                 color: arcade.Color):
        super(Bottle, self).__init__()

        self.x = x
        self.y = y
        self.radius = radius

        # visualisation
        self.center_x = None
        self.center_y = None
        self.color = color
        self.points = None
        self.shape = None
        self.poly = None

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        radius = config['radius']
        color = eval(config['color'])

        return cls(x, y, radius, color)

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, scale):
        self.center_x = self.x * scale
        self.center_y = self.y * scale
        self.points = self._create_points(scale)
        self.shape = self._create_shape()
        self.poly = self._create_poly(scale)

    def _create_points(self, scale) -> PointList:
        """
        Create a list of points representing this bottle in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.radius * scale)

    def _create_shape(self) -> Shape:
        """
        Create a shape representing the circle of this bottle.
        :return: a Arcade shape object.
        """

        color_list = [self.color] + [self.color] * (32 + 1)
        return arcade.create_line_generic_with_colors(self.points, color_list, 6)

    def _create_poly(self, scale) -> Circle:
        """
        Create the polygon used for ray-casting. (Ultrasonic sensor)
        :return: a Pymunk Circle object.
        """

        body = Body(body_type=Body.STATIC)
        body.position = Vec2d(self.center_x, self.center_y)

        return Circle(body, self.radius * scale)
