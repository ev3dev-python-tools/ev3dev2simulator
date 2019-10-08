from ev3dev2.simulator.robot import Robot
from ev3dev2.simulator.robot.BodyPart import BodyPart
from ev3dev2.simulator.util.Util import apply_scaling


class ColorSensor(BodyPart):
    """
    Class representing a ColorSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        super(ColorSensor, self).__init__(address,
                                          img_cfg['color_sensor'],
                                          apply_scaling(0.26),
                                          robot,
                                          delta_x,
                                          delta_y)


    def get_sensed_color(self) -> int:

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return o.color_code

        return self.get_default_value()


    def get_default_value(self):
        """
        6 is the color of white for the real robot. Playing field surface is white.
        :return: integer value representing the color white.
        """

        return 6
