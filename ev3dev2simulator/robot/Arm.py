from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart


class Arm(BodyPart):
    """
    Class representing the body of the simulated robot.
    """


    def __init__(self,
                 img_cfg,
                 robot: Robot,
                 center_x: int,
                 center_y: int):
        super(Arm, self).__init__('', robot, center_x, center_y)
        self.init_texture(img_cfg['arm'], 0.41)
