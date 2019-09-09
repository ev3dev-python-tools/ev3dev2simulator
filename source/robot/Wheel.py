from source.robot.Body import Body
from source.robot.ExtraBodyPart import ExtraBodyPart


class Wheel(ExtraBodyPart):

    def __init__(self,
                 img_cfg,
                 body: Body,
                 delta_x: int,
                 delta_y: int):
        super().__init__(img_cfg['wheel'], 0.25, body, delta_x, delta_y)
