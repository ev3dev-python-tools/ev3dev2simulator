import arcade

from source.robot.Body import Body
from source.robot.ExtraBodyPart import ExtraBodyPart


class ColorSensor(ExtraBodyPart):

    def __init__(self,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int):
        super().__init__(img_cfg['color_sensor'], 0.25, body, delta_x, delta_y)

        blue_texture = arcade.load_texture(img_cfg['color_sensor_blue'], scale=0.25)
        green_texture = arcade.load_texture(img_cfg['color_sensor_green'], scale=0.25)
        red_texture = arcade.load_texture(img_cfg['color_sensor_red'], scale=0.25)

        self.textures = []
        self.textures.append(blue_texture)
        self.textures.append(green_texture)
        self.textures.append(red_texture)
        self.cur_texture_index = 3
