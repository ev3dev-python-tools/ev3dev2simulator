"""
The module arm contains the small arm that is attached to the robot and not the one displayed in the sidebar.
"""

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.arm_large import ArmLarge
from ev3dev2simulator.robotpart.body_part import BodyPart
from ev3dev2simulator.util.dimensions import Dimensions


class Arm(BodyPart):
    """
    Class representing the Arm of the simulated robot.
    """
    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['arm']
        super(Arm, self).__init__(config, robot, Dimensions(dims['width'], dims['height']),
                                  'arm', driver_name='lego-ev3-m-motor')
        self.side_bar_arm = ArmLarge()

    def setup_visuals(self, scale):
        """
        Setup the visuals of the arm of the robot.
        """
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['arm'], scale)

    def rotate_arm(self, degrees):
        """
        Rotates the arm. As this cannot be seen on the robot, it is handled by the one displayed in the sidebar.
        """
        self.side_bar_arm.rotate(degrees)

    def reset(self):
        """
        Reset the robot arm, by resetting the rotation of the arm shown in the sidebar.
        """
        self.side_bar_arm.reset()
