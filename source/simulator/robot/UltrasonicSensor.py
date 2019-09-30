from source.simulator.robot.Body import Body
from source.simulator.robot.ExtraBodyPart import ExtraBodyPart


class UltrasonicSensor(ExtraBodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot.
    """


    def __init__(self,
                 address: str,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int):
        super(UltrasonicSensor, self).__init__(address,
                                               img_cfg['ultrasonic_sensor'],
                                               0.13,
                                               body,
                                               delta_x,
                                               delta_y)
