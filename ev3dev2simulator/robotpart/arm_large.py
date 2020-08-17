"""
The arm_large module contains the class ArmLarge that simulated the arms as seen from above.
"""

import math

from arcade import Sprite
import arcade

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.obstacle.arm_floor import ArmFloor


class ArmLarge(Sprite):
    """
    Class representing the arm as seen from above in the sidebar.
    """

    def __init__(self):
        super(ArmLarge, self).__init__()

        self.x = None
        self.y = None
        self.rotate_x = None
        self.rotate_y = None
        self.side_bar_ground = ArmFloor(300, 10, arcade.color.BLACK)

        self.sweep_length = 229 / 4

    def reset(self):
        """
        Reset the orientation of the arm.
        """
        self.angle = 20
        self.rotate(0)

    def draw(self):
        """
        Draws the ground of the arm and the arm itself.
        """
        self.side_bar_ground.shape.draw()
        super(ArmLarge, self).draw()

    def setup_visuals(self, x, y, width, height):
        """
        Setup the visuals of the robot arm and add a bottom border to it.
        """
        self.center_x = x
        self.center_y = y
        self.rotate_x = x
        self.rotate_y = y + self.sweep_length
        vis_conf = get_simulation_settings()
        self.init_texture(vis_conf['image_paths']['arm_large'], width, height)
        self.side_bar_ground.create_shape(x, y - 70, width, 10)
        self.angle = 0
        self.rotate(20)

    def init_texture(self, src, width, height):
        """
        Initialize the texture base on the give source and dimensions.
        """
        texture = arcade.load_texture(src)

        self.textures.append(texture)
        self.set_texture(0)
        self.height = height
        self.width = width

    def rotate(self, degrees: float):
        """
        Rotate this part by the given angle in radians. Make sure it
        stays 'attached' to its body by also adjusting its x and y values.
        :param degrees: to rotate.
        """
        self.angle += degrees

        rad = math.radians(self.angle)

        self.x = self.sweep_length * math.sin(-rad) + self.rotate_x
        self.y = self.sweep_length * math.cos(-rad) + self.rotate_y
