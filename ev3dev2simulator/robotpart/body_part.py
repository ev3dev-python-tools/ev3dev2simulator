"""
The body_part module contains the class BodyPart, the super class to a all body parts.
"""

import pymunk

from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.util.point import Point
from ev3dev2simulator.visualisation.robot_part_sprite import RobotPartSprite

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

# Default mass used for sprites
DEFAULT_MASS = 5


class BodyPart:
    """
    Class containing the base functionality of a part of the robot.
    """

    def __init__(self, config, robot, dimensions: Dimensions, ev3type, offset=Point(0.0, 0.0), driver_name=None):
        self.name = config['name'] if 'name' in config else 'unnamed'
        self.ev3type = ev3type
        self.brick = int(config['brick'])
        self.address = config['port'] if 'port' in config else 'no_address'
        self.robot = robot
        self.driver_name = driver_name

        self.width_mm = dimensions.width
        self.height_mm = dimensions.height
        self.x_offset = float(config['x_offset']) + offset.x
        self.y_offset = float(config['y_offset']) + offset.y

        self.sensible_obstacles = []

        self.sprite = None
        self.shape = None

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

    def setup_visuals(self, scale):
        """
        Abstract function for settings up the sprite of body part.
        """

    def setup_pymunk_shape(self, px_mm_scale, body):
        """
        Create the shape of a body part as a square.
        """
        width = self.width_mm * px_mm_scale
        height = self.height_mm * px_mm_scale
        vertices = [(0, 0), (width, 0), (width, height), (0, height)]
        transform = pymunk.Transform(tx=self.x_offset * px_mm_scale - width/2,
                                     ty=self.y_offset * px_mm_scale - height/2)
        self.shape = pymunk.Poly(body, vertices, transform=transform)
        self.shape.friction = DEFAULT_FRICTION
        self.shape.mass = DEFAULT_MASS

    def init_sprite_with_list(self, src_list, scale, start_sprite=0):
        """
        Initializes the sprite with a list of textures and the start texture.
        """
        self.sprite = RobotPartSprite(src_list, start_sprite, self.width_mm, scale=scale)

    def init_sprite(self, src, scale):
        """
        Initialize a sprite with only one texture.
        """
        self.init_sprite_with_list([src], scale)

    def get_ev3type(self):
        """
        Get the ev3dev type of the part such as ultrasonic_sensor
        """
        return self.ev3type
