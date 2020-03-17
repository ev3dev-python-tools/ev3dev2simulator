from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.robot.BodyPart import BodyPart


class TouchSensor(BodyPart):
    """
    Class representing a TouchSensor of the simulated robot.
    """

    def __init__(self,
                 brick: int,
                 address: str,
                 robot,
                 delta_x: int,
                 delta_y: int,
                 side: str,
                 name: str):
        super(TouchSensor, self).__init__(brick, address, robot, delta_x, delta_y, 'touch_sensor')
        self.side = side
        self.name = name

    def setup_visuals(self, scale):
        if self.side == 'left':
            img = 'touch_sensor_left'
        elif self.side == 'right':
            img = 'touch_sensor_right'
        else:
            img = 'touch_sensor_rear'
        vis_conf = get_config().get_visualisation_config()
        self.init_texture(vis_conf['image_paths'][img], scale * 0.32)

    def get_latest_value(self):
        return self.is_touching()

    def is_touching(self) -> bool:
        """
        Check if this TouchSensor is touching a TouchObstacle.
        :return: boolean value representing the outcome.
        """
        for o in self.sensible_obstacles:
            if o.collided_with(self):
                return True

        return self.get_default_value()

    def get_default_value(self):
        return False
