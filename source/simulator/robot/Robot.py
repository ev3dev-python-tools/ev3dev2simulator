import math

from arcade import Sprite

from simulator.obstacle import Obstacle
from simulator.robot.UltrasonicSensor import UltrasonicSensor
from simulator.util.Util import calc_differential_steering_angle_x_y
from source.simulator.robot.Body import Body
from source.simulator.robot.ColorSensor import ColorSensor
from source.simulator.robot.TouchSensor import TouchSensor
from source.simulator.robot.Wheel import Wheel


class Robot:

    def __init__(self, cfg, center_x: int, center_y: int):

        img_cfg = cfg['image_paths']
        alloc_cfg = cfg['alloc_settings']

        address_left_motor = alloc_cfg['motor']['left']
        address_right_motor = alloc_cfg['motor']['right']
        address_center_cs = alloc_cfg['color_sensor']['center']
        address_left_cs = alloc_cfg['color_sensor']['left']
        address_right_cs = alloc_cfg['color_sensor']['right']
        address_left_ts = alloc_cfg['touch_sensor']['left']
        address_right_ts = alloc_cfg['touch_sensor']['right']
        address_us = alloc_cfg['ultrasonic_sensor']['top']

        self.wheel_distance = cfg['wheel_settings']['spacing']

        self.body = Body(img_cfg, center_x, center_y)
        self.left_wheel = Wheel(address_left_motor, img_cfg, self.body, (self.wheel_distance / -2), 1)
        self.right_wheel = Wheel(address_right_motor, img_cfg, self.body, (self.wheel_distance / 2), 1)

        self.center_color_sensor = ColorSensor(address_center_cs, img_cfg, self.body, 0, 69)
        # self.left_color_sensor = ColorSensor(address_left_cs, img_cfg, self.body, -45, 70)
        # self.right_color_sensor = ColorSensor(address_right_cs, img_cfg, self.body, 45, 70)

        self.left_touch_sensor = TouchSensor(address_left_ts, img_cfg, self.body, -50, 83, True)
        self.right_touch_sensor = TouchSensor(address_right_ts, img_cfg, self.body, 50, 83, False)

        self.ultrasonic_sensor = UltrasonicSensor(address_us, img_cfg, self.body, 0, -46)

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


    def execute_movement(self, left_ppf: float, right_ppf: float):
        distance_left = left_ppf if left_ppf is not None else 0
        distance_right = right_ppf if right_ppf is not None else 0

        cur_angle = math.radians(self.body.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(self.wheel_distance,
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
