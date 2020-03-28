import arcade

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robot.BodyPart import BodyPart


class Speaker(BodyPart):
    """
    Class representing the Arm of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 robot,
                 center_x: int,
                 center_y: int):
        config = {
            'brick': brick,
            'x_offset': center_x,
            'y_offset': center_y,
            'port': 'speaker'
        }

        dims = get_simulation_settings()['body_part_sizes']['speaker']
        super(Speaker, self).__init__(config, robot, dims['width'], dims['height'], 'speaker')
        print(self.ev3type)

    def setup_visuals(self, scale, body):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['led_black'], scale, body)
