"""
The wheel module contains the class Wheel which represents a wheel of an ev3dev2 robot.
"""

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.body_part import BodyPart
from ev3dev2simulator.util.dimensions import Dimensions


class Wheel(BodyPart):
    """
    Class representing a Wheel of the simulated robot.
    """

    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['wheel']
        super().__init__(config, robot, Dimensions(dims['width'], dims['height']), 'motor',
                         driver_name='lego-ev3-l-motor')

    def setup_visuals(self, scale):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['wheel'], scale)

    def is_falling(self) -> bool:
        """
        Check if this Wheel is 'falling' of the playing field.
        :return: boolean value representing the outcome.
        """
        for obstacle in self.sensible_obstacles:
            if obstacle.collided_with(self.sprite.center_x, self.sprite.center_y):
                return True

        return self.get_default_value()

    def get_default_value(self):
        return False
