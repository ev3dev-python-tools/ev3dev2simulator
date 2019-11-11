from ev3dev2.simulator.robot import Robot
from ev3dev2.simulator.robot.BodyPart import BodyPart


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
        super(ColorSensor, self).__init__(address, robot, delta_x, delta_y)
        self.init_texture(img_cfg['color_sensor'], 0.26)


    def get_sensed_color(self) -> int:
        """
        Get the color this ColorSensor is currently 'seeing'.
        :return: integer value representing the color.
        """

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return o.color_code

        return self.get_default_value()


    def get_default_value(self):
        """
        1 is the color of black for the real robot. Playing field surface is black.
        :return: integer value representing the color black.
        """

        return 1
