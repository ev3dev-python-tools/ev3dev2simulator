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
        dims = get_simulation_settings()['body_part_sizes']['speaker']
        super(Speaker, self).__init__(brick, 'speaker', robot, center_x, center_y,  dims['width'], dims['height'],
                                      'speaker')

    def setup_visuals(self, scale, body):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['led_black'], scale, body)
