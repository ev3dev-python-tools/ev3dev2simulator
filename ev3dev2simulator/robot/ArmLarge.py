import math

from arcade import Sprite, arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.util.Util import apply_scaling


class ArmLarge(Sprite):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self,
                 center_x: int,
                 center_y: int):
        super(ArmLarge, self).__init__()

        self.center_x = center_x
        self.center_y = center_y

        self.sweep_length = apply_scaling(229) / 4

        self.rotate_x = center_x
        self.rotate_y = center_y - self.sweep_length

        self.rotate(20)

    def setup_visuals(self):
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['arm_large'], 0.50)

    def init_texture(self, src, scale):
        texture = arcade.load_texture(src, scale=apply_scaling(scale))

        self.textures.append(texture)
        self.set_texture(0)

    def rotate(self, degrees: float):
        """
        Rotate this part by the given angle in radians. Make sure it
        stays 'attached' to its body by also adjusting its x and y values.
        :param degrees: to rotate.
        """

        self.angle += degrees

        rad = math.radians(self.angle)

        self.center_x = self.sweep_length * math.sin(-rad) + self.rotate_x
        self.center_y = self.sweep_length * math.cos(-rad) + self.rotate_y

    def move_x(self, distance: float):
        pass

    def move_y(self, distance: float):
        pass
