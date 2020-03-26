import math

from arcade import Sprite
import arcade

from ev3dev2simulator.config.config import get_simulation_settings
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

    def setup_visuals(self, x, y, width, height):
        self.center_x = x
        self.center_y = y
        self.rotate_x = x
        self.rotate_y = y + self.sweep_length
        vis_conf = get_simulation_settings()
        self.init_texture(vis_conf['image_paths']['arm_large'], width, height)
        self.side_bar_ground.create_shape(x, y - 70, width, 10)
        self.rotate(20)

    def init_texture(self, src, width, height):
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

    def calculate_drawing_position(self, scale):
        self.center_x = self.x
        self.center_y = self.y

    def move_x(self, distance: float):
        pass

    def move_y(self, distance: float):
        pass
