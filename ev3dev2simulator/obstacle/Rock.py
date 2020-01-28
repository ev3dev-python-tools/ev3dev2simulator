import arcade
from arcade import Shape, PointList
from pymunk import Body, Poly, Vec2d

from ev3dev2simulator.obstacle.TouchObstacle import TouchObstacle


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
        self.color = color
        self.angle = angle

        self.points = self._create_points()
        self.shape = self._create_shape()
        self.poly = self._create_poly()


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
