import math

from source.simulator.robot.BodyPart import BodyPart


class Body(BodyPart):
    """
    Class representing the body of the simulated robot.
    """


    def __init__(self,
                 img_cfg,
                 center_x: int,
                 center_y: int):
        super(Body, self).__init__(img_cfg['body'], 0.10)

        self.center_x = center_x
        self.center_y = center_y


    def rotate(self, radians: float):
        self.angle += math.degrees(radians)
