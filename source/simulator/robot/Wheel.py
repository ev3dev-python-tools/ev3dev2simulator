from simulator.robot import Robot
from source.simulator.robot.BodyPart import BodyPart


class Wheel(BodyPart):
    """
    Class representing a Wheel of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(Wheel, self).__init__(address,
                                    img_cfg['wheel'],
                                    0.22,
                                    robot,
                                    delta_x,
                                    delta_y)
