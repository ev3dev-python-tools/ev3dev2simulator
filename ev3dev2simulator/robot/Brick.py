from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot.BodyPart import BodyPart


class Brick(BodyPart):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 robot,
                 delta_x: int,
                 delta_y: int,
                 name: str):
        self.name = name
        dims = get_config().get_visualisation_config()['body_part_sizes']['body']
        super(Brick, self).__init__(brick, '', robot, delta_x, delta_y, dims['width'], dims['height'], 'brick')

    def setup_visuals(self, scale):
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['body'], scale)
