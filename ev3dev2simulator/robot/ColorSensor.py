import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart
from ev3dev2simulator.util.Util import apply_scaling

COLORS = dict()
COLORS[1] = 0
COLORS[2] = 1
COLORS[3] = 2
COLORS[4] = 5
COLORS[5] = 3
COLORS[6] = 4


class ColorSensor(BodyPart):
    """
    Class representing a ColorSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(ColorSensor, self).__init__(address, robot, delta_x, delta_y)
        self.large_sim_type = get_config().is_large_sim_type()

        black_texture = arcade.load_texture(img_cfg['color_sensor_black'], scale=apply_scaling(0.26))
        blue_texture = arcade.load_texture(img_cfg['color_sensor_blue'], scale=apply_scaling(0.26))
        green_texture = arcade.load_texture(img_cfg['color_sensor_green'], scale=apply_scaling(0.26))
        red_texture = arcade.load_texture(img_cfg['color_sensor_red'], scale=apply_scaling(0.26))
        white_texture = arcade.load_texture(img_cfg['color_sensor_white'], scale=apply_scaling(0.26))
        yellow_texture = arcade.load_texture(img_cfg['color_sensor_yellow'], scale=apply_scaling(0.26))

        self.textures.append(black_texture)
        self.textures.append(blue_texture)
        self.textures.append(green_texture)
        self.textures.append(red_texture)
        self.textures.append(white_texture)
        self.textures.append(yellow_texture)

        self.old_texture_index = 0
        self.set_texture(0)


    def get_sensed_color(self) -> int:
        """
        Get the color this ColorSensor is currently 'seeing'.
        :return: integer value representing the color.
        """

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return o.color_code

        return self.get_default_value()


    def get_default_value(self):
        """
        1 is the color of black for the real robot. Playing field surface is black.
        :return: integer value representing the color black.
        """

        return 1 if self.large_sim_type else 6


    def set_color_texture(self, color):
        converted = COLORS[color]

        if self.old_texture_index != converted:
            self.old_texture_index = converted
            self.set_texture(converted)
