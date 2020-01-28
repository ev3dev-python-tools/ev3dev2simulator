import math

import arcade

from ev3dev2simulator.robot import Robot
from ev3dev2simulator.util.Util import pythagoras, apply_scaling


class BodyPart(arcade.Sprite):
    """
    Class containing the base functionality of a part of the robot.
    """


    def __init__(self,
                 address: str,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(BodyPart, self).__init__()

        self.address = address
        self.robot = robot
        self.center_x = robot.wheel_center_x + delta_x
        self.center_y = robot.wheel_center_y + delta_y

        self.angle_addition = -math.atan(delta_x / delta_y)
        self.sweep_length = pythagoras(delta_x, delta_y)

        if delta_y < 0:
            self.angle_addition += math.radians(180)

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


    def rotate(self, radians: float):
        """
        Rotate this part by the given angle in radians. Make sure it
        stays 'attached' to its body by also adjusting its x and y values.
        :param radians: to rotate.
        """

        self.angle += math.degrees(radians)

        rad = math.radians(self.angle) + self.angle_addition

        self.center_x = self.sweep_length * math.sin(-rad) + self.robot.wheel_center_x
        self.center_y = self.sweep_length * math.cos(-rad) + self.robot.wheel_center_y


    def set_sensible_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected via collision detection by this body part.
        :param obstacles: to be detected.
        """

        self.sensible_obstacles = obstacles


    def get_default_value(self):
        """
        Get the default value which the sensor would return without
        any interaction with the world.
        :return: any possible value representing the default value.
        """

        pass


    def init_texture(self, src, scale):
        texture = arcade.load_texture(src, scale=apply_scaling(scale))

        self.textures.append(texture)
        self.set_texture(0)
