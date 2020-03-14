from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart


class Arm(BodyPart):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot: Robot,
                 center_x: int,
                 center_y: int):
        vis_conf = get_config().get_visualisation_config()
        super(Arm, self).__init__(brick, address, robot, center_x, center_y, 'wheel')
        self.init_texture(vis_conf['image_paths']['arm'], 0.41)
