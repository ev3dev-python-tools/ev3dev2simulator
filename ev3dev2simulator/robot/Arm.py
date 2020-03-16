import arcade

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.obstacle.Ground import Ground
from ev3dev2simulator.robot.ArmLarge import ArmLarge
from ev3dev2simulator.robot.BodyPart import BodyPart
from ev3dev2simulator.util.Util import apply_scaling


class Arm(BodyPart):
    """
    Class representing the Arm of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 center_x: int,
                 center_y: int):
        super(Arm, self).__init__(brick, address, robot, center_x, center_y, 'arm')
        self.side_bar_arm = ArmLarge(apply_scaling(1450), apply_scaling(1100))
        self.side_bar_ground = Ground(1460, 950, 300, 10,  arcade.color.BLACK)

    def setup_visuals(self):
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths']['arm'], 0.41)

    def rotate_arm(self, degrees):
        self.side_bar_arm.rotate(degrees)
