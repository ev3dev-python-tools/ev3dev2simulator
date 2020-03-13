from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart
from ev3dev2simulator.util.Util import apply_scaling


class Brick(BodyPart):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        vis_conf = get_config().get_visualisation_config()
        super(Brick, self).__init__(brick, '', robot, apply_scaling(delta_x), apply_scaling(delta_y))
        self.init_texture(vis_conf['image_paths']['body'], 0.15)
