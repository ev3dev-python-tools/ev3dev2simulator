from simulator.robot import Robot
from source.simulator.robot.BodyPart import BodyPart


class Body(BodyPart):
    """
    Class representing the body of the simulated robot.
    """


    def __init__(self,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(Body, self).__init__(None,
                                   img_cfg['body'],
                                   0.10,
                                   robot,
                                   delta_x,
                                   delta_y)
