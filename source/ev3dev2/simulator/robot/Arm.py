import math

from arcade import Sprite

from ev3dev2.simulator.util.Util import apply_scaling


class Arm(Sprite):
    """
    Class representing the body of the simulated robot.
    """


    def __init__(self,
                 img_cfg,
                 center_x: int,
                 center_y: int):
        super(Arm, self).__init__(img_cfg['arm'], apply_scaling(0.50))

        self.center_x = center_x
        self.center_y = center_y

        self.sweep_length = 314 * apply_scaling(0.50) / 2
        self.rotate_x = center_x
        self.rotate_y = center_y - self.sweep_length

        self.angle += 20


    def rotate(self, degrees: float):
        """
        Rotate this part by the given angle in radians. Make sure it
        stays 'attached' to its body by also adjusting its x and y values.
        :param degrees: to rotate.
        """

        self.angle += degrees

        rad = math.radians(self.angle)

        self.center_x = self.sweep_length * math.sin(-rad) + self.rotate_x
        self.center_y = self.sweep_length * math.cos(-rad) + self.rotate_y
