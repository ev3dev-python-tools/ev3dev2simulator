from simulator.robot import Robot
from simulator.util.Util import apply_scaling
from source.simulator.robot.BodyPart import BodyPart


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
                 left: bool):
        img = 'touch_sensor_left' if left else 'touch_sensor_right'
        super(TouchSensor, self).__init__(address,
                                          img_cfg[img],
                                          apply_scaling(0.32),
                                          robot,
                                          delta_x,
                                          delta_y)


    def is_touching(self) -> bool:

        for o in self.sensible_obstacles:
            if o.collided_with(self):
                return True

        return False


    def get_default_value(self):
        return False
