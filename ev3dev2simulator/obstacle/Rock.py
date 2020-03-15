import arcade
from arcade import Shape, PointList
from pymunk import Body, Poly, Vec2d

from ev3dev2simulator.obstacle.TouchObstacle import TouchObstacle

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.util.Util import apply_scaling


class Rock(TouchObstacle):
    """
    This class represents a 'rock'. Rocks are rectangles.
    """

    def __init__(self,
                 center_x: int,
                 center_y: int,
                 width: int,
                 height: int,
                 color: arcade.Color,
                 angle: int):
        super(Rock, self).__init__()

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.angle = angle

        # visualisation
        self.color = color
        self.points = None
        self.shape = None
        self.poly = None

    def get_shapes(self):
        if self.shape is None:
            self.create_shape()
        return [self.shape]

    def create_shape(self):
        self.points = self._create_points()
        self.shape = self._create_shape()
        self.poly = self._create_poly()

    @classmethod
    def from_config(cls, config):
        x = apply_scaling(config['x'])
        y = apply_scaling(config['y'])
        width = apply_scaling(config['width'])
        height = apply_scaling(config['height'])
        color = eval(config['color'])
        angle = config['angle']

        return cls(x, y, width, height, color, angle)

    def _create_points(self) -> PointList:
        """
        Create a list of points representing this rock in 2D space.
        :return: a PointList object.
        """

        return arcade.get_rectangle_points(self.center_x,
                                           self.center_y,
                                           self.width,
                                           self.height,
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

    def _create_poly(self):
        """
        Create the polygon used for ray-casting. (Ultrasonic sensor)
        :return: a Pymunk Poly object.
        """

        body = Body(body_type=Body.STATIC)
        body.position = Vec2d(self.center_x, self.center_y)

        return Poly.create_box(body, (self.width, self.height))
