import math

from arcade import Sprite, arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.Ground import Ground


class ArmLarge(Sprite):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self):
        super(ArmLarge, self).__init__()

        self.x = None
        self.y = None
        self.rotate_x = None
        self.rotate_y = None
        self.side_bar_ground = Ground(300, 10, arcade.color.BLACK)

        self.sweep_length = 229 / 4

    def draw(self):
        self.side_bar_ground.shape.draw()
        super(ArmLarge, self).draw()

    def setup_visuals(self, x, y, scale):
        self.center_x = x
        self.center_y = y
        self.rotate_x = x
        self.rotate_y = y + self.sweep_length
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['arm_large'], scale * 0.5)
        self.side_bar_ground.create_shape(x, y - 70, scale)
        self.rotate(20)

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
