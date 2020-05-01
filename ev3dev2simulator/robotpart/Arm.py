from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.ArmLarge import ArmLarge
from ev3dev2simulator.robotpart.BodyPart import BodyPart


class Arm(BodyPart):
    """
    Class representing the Arm of the simulated robotpart.
    """
    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['arm']
        super(Arm, self).__init__(config, robot, dims['width'], dims['height'], 'arm', driver_name='lego-ev3-m-motor')
        self.side_bar_arm = ArmLarge()

    def setup_visuals(self, scale):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['arm'], scale)

    def rotate_arm(self, degrees):
        self.side_bar_arm.rotate(degrees)
