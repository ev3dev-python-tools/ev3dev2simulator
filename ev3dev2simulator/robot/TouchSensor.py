from ev3dev2simulator.robot import Robot
from ev3dev2simulator.robot.BodyPart import BodyPart


class TouchSensor(BodyPart):
    """
    Class representing a TouchSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 robot: Robot,
                 delta_x: int,
                 delta_y: int,
                 side: str):

        if side == 'left':
            img = 'touch_sensor_left'
        elif side == 'right':
            img = 'touch_sensor_right'
        else:
            img = 'touch_sensor_rear'

        super(TouchSensor, self).__init__(address, robot, delta_x, delta_y)
        self.init_texture(img_cfg[img], 0.32)


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
