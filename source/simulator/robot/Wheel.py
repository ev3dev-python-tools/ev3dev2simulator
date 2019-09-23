from source.simulator.robot.Body import Body
from source.simulator.robot.ExtraBodyPart import ExtraBodyPart


class Wheel(ExtraBodyPart):

    def __init__(self,
                 address: str,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int):
        super().__init__(address,
                         img_cfg['wheel'],
                         0.22,
                         body,
                         delta_x,
                         delta_y)
