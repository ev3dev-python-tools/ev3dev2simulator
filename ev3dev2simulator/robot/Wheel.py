from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart


class Wheel(BodyPart):
    """
    Class representing a Wheel of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int):
        vis_conf = get_config().get_visualisation_config()
        super(Wheel, self).__init__(brick, address, robot, delta_x, delta_y, 'motor')
        self.init_texture(vis_conf['image_paths']['wheel'], 0.33)

    def is_falling(self) -> bool:
        """
        Check if this Wheel is 'falling' of the playing field.
        :return: boolean value representing the outcome.
        """

        for o in self.sensible_obstacles:
            if o.collided_with(self.center_x, self.center_y):
                return True

        return self.get_default_value()

    def get_default_value(self):
        return False
