import arcade

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robot.BodyPart import BodyPart


class TouchSensor(BodyPart):
    """
    Class representing a TouchSensor of the simulated robot.
    """
    def __init__(self, config: dict, robot):
        self.side = config['side']
        if self.side in ['left', 'right']:
            dims = get_simulation_settings()['body_part_sizes']['touch_sensor_bar']
        else:
            dims = get_simulation_settings()['body_part_sizes']['touch_sensor_bar_rear']

        super(TouchSensor, self).__init__(config, robot, dims['width'], dims['height'], 'touch_sensor')

    def setup_visuals(self, scale):
        if self.side == 'left':
            img = 'touch_sensor_left'
        elif self.side == 'right':
            img = 'touch_sensor_right'
        else:
            img = 'touch_sensor_rear'
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths'][img], scale)

    def get_latest_value(self):
        return self.is_touching()

    def is_touching(self) -> bool:
        """
        Check if this TouchSensor is touching a TouchObstacle.
        :return: boolean value representing the outcome.
        """
        if self.sprite is None:
            return False
        if arcade.check_for_collision_with_list(self.sprite, self.sensible_obstacles):
            return True

        return self.get_default_value()

    def get_default_value(self):
        return False
