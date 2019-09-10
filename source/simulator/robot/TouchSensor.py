from source.simulator.robot.Body import Body
from source.simulator.robot.ExtraBodyPart import ExtraBodyPart


class TouchSensor(ExtraBodyPart):

    def __init__(self,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int,
                 left: bool):
        img = 'touch_sensor_left' if left else 'touch_sensor_right'
        super().__init__(img_cfg[img], 0.25, body, delta_x, delta_y)
