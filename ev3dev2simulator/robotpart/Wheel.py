from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.BodyPart import BodyPart


class Wheel(BodyPart):
    """
    Class representing a Wheel of the simulated robotpart.
    """

    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['wheel']
        super().__init__(config, robot, int(dims['width']), int(dims['height']), 'motor',
                         driver_name='lego-ev3-l-motor')

    def setup_visuals(self, scale):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['wheel'], scale)

    def is_falling(self) -> bool:
        """
        Check if this Wheel is 'falling' of the playing field.
        :return: boolean value representing the outcome.
        """
        for o in self.sensible_obstacles:
            if o.collided_with(self.sprite.center_x, self.sprite.center_y):
                return True

        return self.get_default_value()

    def get_default_value(self):
        return False
