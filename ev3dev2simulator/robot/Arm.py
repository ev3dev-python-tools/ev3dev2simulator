from ev3dev2simulator.config.config import get_simulation_settings
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
        dims = get_simulation_settings()['body_part_sizes']['arm']
        super(Arm, self).__init__(brick, address, robot, x, y, dims['width'], dims['height'],  'arm')
        self.side_bar_arm = ArmLarge()

    def setup_visuals(self, scale, body):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['arm'], scale, body=body)

    def rotate_arm(self, degrees):
        self.side_bar_arm.rotate(degrees)
