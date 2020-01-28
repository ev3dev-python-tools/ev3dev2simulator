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
                 center_x: int,
                 center_y: int,
                 radius: float,
                 color: arcade.Color):
        super(Bottle, self).__init__()

        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color

        self.points = self._create_points()
        self.shape = self._create_shape()
        self.poly = self._create_poly()


    def _create_points(self) -> PointList:
        """
        Create a list of points representing this bottle in 2D space.
        :return: a PointList object.
        """

        return get_circle_points(self.center_x,
                                 self.center_y,
                                 self.radius)


    def _create_shape(self) -> Shape:
        """
        Create a shape representing the circle of this bottle.
        :return: a Arcade shape object.
        """

        color_list = [self.color] + [self.color] * (32 + 1)
        return arcade.create_line_generic_with_colors(self.points, color_list, 6)


    def _create_poly(self) -> Circle:
        """
        Create the polygon used for ray-casting. (Ultrasonic sensor)
        :return: a Pymunk Circle object.
        """

        body = Body(body_type=Body.STATIC)
        body.position = Vec2d(self.center_x, self.center_y)

        return Circle(body, self.radius)
