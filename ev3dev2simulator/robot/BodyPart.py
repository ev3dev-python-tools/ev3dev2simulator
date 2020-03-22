import math
import arcade

from ev3dev2simulator.util.Util import pythagoras


class BodyPart(arcade.Sprite):
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
        super(BodyPart, self).__init__()

        self.ev3type = ev3type
        self.brick = brick
        self.address = address
        self.robot = robot
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.x = robot.x + delta_x
        self.y = robot.y + delta_y
        self.px_mm_scale = None

        self.angle_addition = -math.atan(delta_x / delta_y) if delta_y else 0
        self.sweep_length = pythagoras(delta_x, delta_y)

        if delta_y < 0:
            self.angle_addition += math.radians(180)

        self.sensible_obstacles = []

    def calculate_drawing_position(self, scale):
        self.center_x = self.x * scale
        self.center_y = self.y * scale

    def move_x(self, distance: float):
        """
        Move this part by the given distance in the x-direction.
        :param distance: to move
        """

        self.x += distance

    def move_y(self, distance: float):
        """
        Move this part by the given distance in the y-direction.
        :param distance: to move
        """

        self.y += distance

    def rotate(self, radians: float):
        """
        Rotate this part by the given angle in radians. Make sure it
        stays 'attached' to its body by also adjusting its x and y values.
        :param radians: to rotate.
        """

        self.angle += math.degrees(radians)

        rad = math.radians(self.angle) + self.angle_addition

        self.x = self.sweep_length * math.sin(-rad) + self.robot.x
        self.y = self.sweep_length * math.cos(-rad) + self.robot.y

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

    def setup_visuals(self, scale):
        pass

    def init_texture_list(self, src_list, scale, start_sprite=0):
        for texture in src_list:
            texture = arcade.load_texture(texture)
            self.append_texture(texture)

        self.set_texture(start_sprite)
        self.px_mm_scale = scale
        self.set_dimensions(self.width_mm, self.height_mm, scale)
        self._set_hit_box_based_on_mm(scale)

    def init_texture(self, src, scale):

        texture = arcade.load_texture(src)
        self.append_texture(texture)
        self.set_texture(0)
        self.px_mm_scale = scale
        self.set_dimensions(self.width_mm, self.height_mm, scale)
        self._set_hit_box_based_on_mm(scale)

    def set_dimensions(self, new_width, new_height, scale):
        self.height = new_height * scale
        self.width = new_width * scale

    def get_ev3type(self):
        return self.ev3type

    def _set_hit_box_based_on_mm(self, scale):
        full_scale = (self.width_mm / self.texture.width) * scale
        self.hit_box = [(x * full_scale, y * full_scale) for (x, y) in self.texture.hit_box_points]

