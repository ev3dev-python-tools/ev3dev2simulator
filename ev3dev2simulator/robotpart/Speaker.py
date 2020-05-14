from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.BodyPart import BodyPart


class Speaker(BodyPart):
    """
    Class representing the Arm of the simulated robotpart.
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

    def setup_visuals(self, scale):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['led_black'], scale)
