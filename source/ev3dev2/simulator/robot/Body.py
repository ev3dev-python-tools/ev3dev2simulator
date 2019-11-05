from ev3dev2.simulator.robot import Robot
from ev3dev2.simulator.robot.BodyPart import BodyPart
from ev3dev2.simulator.util.Util import apply_scaling


class Body(BodyPart):
    """
    Class representing the body of the simulated robot.
    """


    def __init__(self,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(Body, self).__init__('',
                                   img_cfg['body'],
                                   apply_scaling(0.15),
                                   robot,
                                   delta_x,
                                   delta_y)
