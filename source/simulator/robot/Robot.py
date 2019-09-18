import math

from arcade import Sprite

from simulator.job.MoveJob import MoveJob
from simulator.obstacle import Obstacle
from simulator.robot.UltrasonicSensor import UltrasonicSensor
from simulator.util.Util import calc_differential_steering_angle_x_y
from source.simulator.robot.Body import Body
from source.simulator.robot.ColorSensor import ColorSensor
from source.simulator.robot.TouchSensor import TouchSensor
from source.simulator.robot.Wheel import Wheel

WHEEL_DISTANCE = 80


class Robot:

    def __init__(self, img_cfg, center_x: int, center_y: int):

        self.body = Body(img_cfg, center_x, center_y)
        self.left_wheel = Wheel(img_cfg, self.body, -40, 1)
        self.right_wheel = Wheel(img_cfg, self.body, 40, 1)

        self.center_color_sensor = ColorSensor(img_cfg, self.body, 0, 69)
        # self.left_color_sensor = ColorSensor(img_cfg, self.body, -45, 70)
        # self.right_color_sensor = ColorSensor(img_cfg, self.body, 45, 70)

        self.left_touch_sensor = TouchSensor(img_cfg, self.body, -50, 83, True)
        self.right_touch_sensor = TouchSensor(img_cfg, self.body, 50, 83, False)

        self.ultrasonic_sensor = UltrasonicSensor(img_cfg, self.body, 0, -46)

        self.sprites = [self.body,
                        self.left_wheel,
                        self.right_wheel,
                        self.center_color_sensor,
                        # self.left_color_sensor,
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


    def execute_move_job(self, left_job: MoveJob, right_job: MoveJob):
        distance_left = left_job.distance if left_job is not None else 0
        distance_right = right_job.distance if right_job is not None else 0

        cur_angle = math.radians(self.body.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(WHEEL_DISTANCE,
                                                 distance_left,
                                                 distance_right,
                                                 cur_angle)

        self._rotate(diff_angle)
        self._move_x(diff_x)
        self._move_y(diff_y)


    def get_sprites(self) -> [Sprite]:
        return self.sprites


    def set_color_obstacles(self, obstacles: [Obstacle]):
        self.center_color_sensor.set_sensible_obstacles(obstacles)
        # self.left_color_sensor.set_sensible_obstacles(obstacles)
        # self.right_color_sensor.set_sensible_obstacles(obstacles)


    def set_touch_obstacles(self, obstacles: [Obstacle]):
        self.left_touch_sensor.set_sensible_obstacles(obstacles)
        self.right_touch_sensor.set_sensible_obstacles(obstacles)
