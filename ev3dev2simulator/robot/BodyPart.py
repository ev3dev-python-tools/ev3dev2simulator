import math
from pymunk import Vec2d

from ev3dev2simulator.visualisation.PymunkRobotPartSprite import PymunkRobotPartSprite


class BodyPart:
    """
    Class containing the base functionality of a part of the robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 delta_x: int,
                 delta_y: int,
                 width_mm: int,
                 height_mm: int,
                 ev3type: str):
        self.ev3type = ev3type
        self.brick = brick
        self.address = address
        self.robot = robot
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.x = robot.x + delta_x
        self.y = robot.y + delta_y

        self.x_offset = delta_x
        self.y_offset = delta_y

        self.angle_addition = -math.atan(delta_x / delta_y) if delta_y else 0
        self.sweep_length = math.hypot(delta_x, delta_y)

        if delta_y < 0:
            self.angle_addition += math.radians(180)

        self.sensible_obstacles = []

        self.sprite = None

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

    def setup_visuals(self, scale, body):
        pass

    def init_sprite_with_list(self, src_list, scale, start_sprite=0, body=None):
        self.sprite = PymunkRobotPartSprite(src_list, start_sprite, self.x_offset, self.y_offset,
                                            self.width_mm, self.height_mm, scale=scale, body=body)

    def init_sprite(self, src, scale, body):
        self.init_sprite_with_list([src], scale, body=body)

    def get_ev3type(self):
        return self.ev3type
