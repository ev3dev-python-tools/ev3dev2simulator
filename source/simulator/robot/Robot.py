import math

from arcade import Sprite

from simulator.job.MoveJob import MoveJob
from simulator.robot.UltrasonicSensor import UltrasonicSensor
from simulator.util.Util import calc_differential_steering_angle_x_y
from source.simulator.robot.Body import Body
from source.simulator.robot.ColorSensor import ColorSensor
from source.simulator.robot.TouchSensor import TouchSensor
from source.simulator.robot.Wheel import Wheel

WHEEL_DISTANCE = 90


class Robot:
    def __init__(self, img_cfg, center_x: int, center_y: int):

        self.body = Body(img_cfg, center_x, center_y)
        self.left_wheel = Wheel(img_cfg, self.body, -40, 1)
        self.right_wheel = Wheel(img_cfg, self.body, 40, 1)

        # self.left_color_sensor = ColorSensor(img_cfg, self.body, -45, 70)
        self.center_color_sensor = ColorSensor(img_cfg, self.body, 0, 69)
        # self.right_color_sensor = ColorSensor(img_cfg, self.body, 45, 70)

        self.left_touch_sensor = TouchSensor(img_cfg, self.body, -50, 83, True)
        self.right_touch_sensor = TouchSensor(img_cfg, self.body, 50, 83, False)

        self.ultrasonic_sensor = UltrasonicSensor(img_cfg, self.body, 0, -46)

        self.sprites = [self.body,
                        self.left_wheel,
                        self.right_wheel,
                        # self.left_color_sensor,
                        self.center_color_sensor,
                        # self.right_color_sensor,
                        self.left_touch_sensor,
                        self.right_touch_sensor,
                        self.ultrasonic_sensor]

    def _move_x(self, x: float):
        for s in self.get_sprites():
            s.move_x(x)

    def _move_y(self, y: float):
        for s in self.get_sprites():
            s.move_y(y)

    def _rotate(self, radians: float):
        for s in self.get_sprites():
            s.rotate(radians)

    def get_sprites(self) -> [Sprite]:
        return self.sprites

    def execute_move_job(self, move_job: MoveJob):
        cur_angle = math.radians(self.body.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(WHEEL_DISTANCE,
                                                 move_job.velocity_right,
                                                 move_job.velocity_left,
                                                 cur_angle)

        self._rotate(diff_angle)
        self._move_x(diff_x)
        self._move_y(diff_y)
