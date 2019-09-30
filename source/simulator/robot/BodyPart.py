import arcade

from simulator.obstacle import Obstacle


class BodyPart(arcade.Sprite):
    """
    Class containing the base functionality of a part of the robot.
    """


    def __init__(self, src: str, scale: float):
        super(BodyPart, self).__init__(src, scale)

        self.sensible_obstacles = None


    def move_x(self, distance: float):
        """
        Move this part by the given distance in the x-direction.
        :param distance: to move
        """

        self.center_x += distance


    def move_y(self, distance: float):
        """
        Move this part by the given distance in the y-direction.
        :param distance: to move
        """

        self.center_y += distance


    def set_sensible_obstacles(self, obstacles: [Obstacle]):
        """
        Set the obstacles which can be detected via collision detection by this body part.
        :param obstacles: to be detected.
        """

        self.sensible_obstacles = obstacles
