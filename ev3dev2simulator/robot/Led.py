import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot.BodyPart import BodyPart


class Led(BodyPart):
    """
    Class representing a Wheel of the simulated robot.
    """
    def __init__(self,
                 brick: int,
                 robot,
                 delta_x: int,
                 delta_y: int):
        dims = get_config().get_visualisation_config()['body_part_sizes']['led']
        super(Led, self).__init__(brick, '', robot, delta_x, delta_y, dims['width'], dims['height'], 'led')
        self.old_texture_index = 1

    def setup_visuals(self, scale):
        img_cfg = get_config().get_visualisation_config()['image_paths']
        src_list = [img_cfg[f'led_{color}'] for color in ['amber', 'black', 'green', 'red', 'orange', 'yellow']]
        self.init_texture_list(src_list, scale, 1)

    def set_color_texture(self, color):
        if self.old_texture_index != color:
            self.old_texture_index = color
            self.set_texture(color)
            self.set_dimensions(self.width_mm, self.height_mm, self.px_mm_scale)
