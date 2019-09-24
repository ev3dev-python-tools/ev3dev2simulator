import arcade

from simulator.obstacle import Obstacle


class BodyPart(arcade.Sprite):

    def __init__(self, src: str, scale: float):
        super(BodyPart, self).__init__(src, scale)

        self.sensible_obstacles = None


    def move_x(self, x: float):
        self.center_x += x


    def move_y(self, y: float):
        self.center_y += y


    def set_sensible_obstacles(self, obstacles: [Obstacle]):
        """
        Set the obstacles which can be detected via collision detection by this body part.
        :param obstacles: to be detected.
        """

        self.sensible_obstacles = obstacles
