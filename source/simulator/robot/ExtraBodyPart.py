import math

from source.simulator.robot.BodyPart import BodyPart
from source.simulator.util.Util import pythagoras


class ExtraBodyPart(BodyPart):

    def __init__(self,
                 src: str,
                 scale: float,
                 body: BodyPart,
                 delta_x: int,
                 delta_y: int):
        super().__init__(src, scale)

        self.body = body
        self.center_x = body.center_x + delta_x
        self.center_y = body.center_y + delta_y

        self.angle_addition = math.atan(delta_x / delta_y)
        self.sweep_length = pythagoras(delta_x, delta_y)

    def rotate(self, degrees: int):
        self.angle += degrees

        rad = math.radians(self.angle) + self.angle_addition

        self.center_x = self.sweep_length * math.sin(-rad) + self.body.center_x
        self.center_y = self.sweep_length * math.cos(-rad) + self.body.center_y
