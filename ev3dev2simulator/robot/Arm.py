import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.Ground import Ground
from ev3dev2simulator.robot.ArmLarge import ArmLarge
from ev3dev2simulator.robot.BodyPart import BodyPart


class Arm(BodyPart):
    """
    Class representing the Arm of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 x: int,
                 y: int):
        super(Arm, self).__init__(brick, address, robot, x, y, 'arm')
        self.side_bar_arm = ArmLarge(1450, 1100)
        self.side_bar_ground = Ground(1460, 950, 300, 10,  arcade.color.BLACK)

    def setup_visuals(self, scale):
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['arm'], scale * 0.41)

    def rotate_arm(self, degrees):
        self.side_bar_arm.rotate(degrees)
