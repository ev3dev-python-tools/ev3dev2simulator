import math

from arcade import Sprite, arcade

from ev3dev2simulator.config.config import get_config


class ArmLarge(Sprite):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self,
                 x: int,
                 y: int):
        super(ArmLarge, self).__init__()

        self.x = x
        self.y = y

        self.sweep_length = 229 / 4

        self.rotate_x = x
        self.rotate_y = y - self.sweep_length

        self.rotate(20)

    def setup_visuals(self, scale):
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['arm_large'], scale * 0.50)

    def init_texture(self, src, scale):
        texture = arcade.load_texture(src, scale=scale)

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

        self.x = self.sweep_length * math.sin(-rad) + self.rotate_x
        self.y = self.sweep_length * math.cos(-rad) + self.rotate_y

    def calculate_drawing_position(self, scale):
        self.center_x = self.x
        self.center_y = self.y

    def move_x(self, distance: float):
        pass

    def move_y(self, distance: float):
        pass
