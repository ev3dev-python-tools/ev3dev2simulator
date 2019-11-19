import math

from arcade import Sprite

from ev3dev2.simulator.obstacle import ColorObstacle
from ev3dev2.simulator.robot import BodyPart
from ev3dev2.simulator.robot.Arm import Arm
from ev3dev2.simulator.robot.ArmLarge import ArmLarge
from ev3dev2.simulator.robot.Body import Body
from ev3dev2.simulator.robot.ColorSensor import ColorSensor
from ev3dev2.simulator.robot.Led import Led
from ev3dev2.simulator.robot.TouchSensor import TouchSensor
from ev3dev2.simulator.robot.UltrasonicSensorBottom import UltrasonicSensorBottom
from ev3dev2.simulator.robot.UltrasonicSensorTop import UltrasonicSensor
from ev3dev2.simulator.robot.Wheel import Wheel
from ev3dev2.simulator.util.Util import apply_scaling, calc_differential_steering_angle_x_y


class Robot:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """


    def __init__(self, cfg, center_x: int, center_y: int, orientation: int):

        self.wheel_center_x = center_x
        self.wheel_center_y = center_y + apply_scaling(22.5)

        img_cfg = cfg['image_paths']
        alloc_cfg = cfg['alloc_settings']

        address_motor_left = alloc_cfg['motor']['left']
        address_motor_right = alloc_cfg['motor']['right']
        address_cs_center = alloc_cfg['color_sensor']['center']
        address_cs_left = alloc_cfg['color_sensor']['left']
        address_cs_right = alloc_cfg['color_sensor']['right']
        address_ts_left = alloc_cfg['touch_sensor']['left']
        address_ts_right = alloc_cfg['touch_sensor']['right']
        address_us_front = alloc_cfg['ultrasonic_sensor']['front']
        address_us_rear = alloc_cfg['ultrasonic_sensor']['rear']

        self.wheel_distance = apply_scaling(cfg['wheel_settings']['spacing'])

        self.left_body = Body(img_cfg, self, apply_scaling(39), apply_scaling(-22.5))
        self.right_body = Body(img_cfg, self, apply_scaling(-39), apply_scaling(-22.5))

        self.arm = Arm(img_cfg, self, apply_scaling(15), apply_scaling(102))
        self.arm_large = ArmLarge(img_cfg, apply_scaling(1450), apply_scaling(1100))

        self.left_wheel = Wheel(address_motor_left, img_cfg, self, (self.wheel_distance / -2), 0.01)
        self.right_wheel = Wheel(address_motor_right, img_cfg, self, (self.wheel_distance / 2), 0.01)

        self.center_color_sensor = ColorSensor(address_cs_center, img_cfg, self, 0, apply_scaling(84))
        self.left_color_sensor = ColorSensor(address_cs_left, img_cfg, self, apply_scaling(-69), apply_scaling(95))
        self.right_color_sensor = ColorSensor(address_cs_right, img_cfg, self, apply_scaling(69), apply_scaling(95))

        self.left_touch_sensor = TouchSensor(address_ts_left, img_cfg, self, apply_scaling(-65), apply_scaling(102), True)
        self.right_touch_sensor = TouchSensor(address_ts_right, img_cfg, self, apply_scaling(65), apply_scaling(102), False)

        self.front_ultrasonic_sensor = UltrasonicSensor(address_us_front, img_cfg, self, apply_scaling(-22), apply_scaling(56))
        self.rear_ultrasonic_sensor = UltrasonicSensorBottom(address_us_rear, img_cfg, self, 0, apply_scaling(-145))

        self.left_brick_left_led = Led(img_cfg, self, apply_scaling(-20), apply_scaling(-55))
        self.left_brick_right_led = Led(img_cfg, self, apply_scaling(-60), apply_scaling(-55))

        self.right_brick_left_led = Led(img_cfg, self, apply_scaling(20), apply_scaling(-55))
        self.right_brick_right_led = Led(img_cfg, self, apply_scaling(60), apply_scaling(-55))

        self.movable_sprites = [self.left_wheel,
                                self.right_wheel,
                                self.left_body,
                                self.right_body,
                                self.center_color_sensor,
                                self.left_color_sensor,
                                self.right_color_sensor,
                                self.left_touch_sensor,
                                self.right_touch_sensor,
                                self.rear_ultrasonic_sensor,
                                self.front_ultrasonic_sensor,
                                self.left_brick_left_led,
                                self.left_brick_right_led,
                                self.right_brick_left_led,
                                self.right_brick_right_led,
                                self.arm]

        self.sprites = self.movable_sprites.copy()
        self.sprites.append(self.arm_large)

        if orientation != 0:
            self._rotate(math.radians(orientation))


    def _move_x(self, distance: float):
        """
        Move all parts of this robot by the given distance in the x-direction.
        :param distance: to move
        """

        for s in self.movable_sprites:
            s.move_x(distance)


    def _move_y(self, distance: float):
        """
        Move all parts of this robot by the given distance in the y-direction.
        :param distance: to move
        """

        for s in self.movable_sprites:
            s.move_y(distance)


    def _rotate(self, radians: float):
        """
        Rotate all parts of this robot by the given angle in radians.
        :param radians to rotate
        """
        for s in self.movable_sprites:
            s.rotate(radians)


    def execute_movement(self, left_ppf: float, right_ppf: float):
        """
        Move the robot and its parts by providing the speed of the left and right motor
        using the differential steering principle.
        :param left_ppf: speed in pixels per second of the left motor.
        :param right_ppf: speed in pixels per second of the right motor.
        """

        distance_left = left_ppf if left_ppf is not None else 0
        distance_right = right_ppf if right_ppf is not None else 0

        cur_angle = math.radians(self.left_body.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(self.wheel_distance,
                                                 distance_left,
                                                 distance_right,
                                                 cur_angle)

        self.wheel_center_x += diff_x
        self.wheel_center_y += diff_y

        self._rotate(diff_angle)
        self._move_x(diff_x)
        self._move_y(diff_y)


    def execute_arm_movement(self, dfp: float):
        """
        Move the robot arm by providing the speed of the center motor.
        :param dfp: speed in degrees per second of the center motor.
        """

        self.arm_large.rotate(dfp)


    def set_left_brick_led_colors(self, left_color, right_color):
        self.left_brick_left_led.set_color_texture(left_color)
        self.left_brick_right_led.set_color_texture(right_color)


    def set_right_brick_led_colors(self, left_color, right_color):
        self.right_brick_left_led.set_color_texture(left_color)
        self.right_brick_right_led.set_color_texture(right_color)


    def set_color_obstacles(self, obstacles: [ColorObstacle]):
        """
        Set the obstacles which can be detected by the color sensors of this robot.
        :param obstacles: to be detected.
        """

        self.center_color_sensor.set_sensible_obstacles(obstacles)
        self.left_color_sensor.set_sensible_obstacles(obstacles)
        self.right_color_sensor.set_sensible_obstacles(obstacles)


    def set_touch_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the touch sensors of this robot.
        :param obstacles: to be detected.
        """

        self.left_touch_sensor.set_sensible_obstacles(obstacles)
        self.right_touch_sensor.set_sensible_obstacles(obstacles)


    def set_falling_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the wheel of this robot. This simulates
        the entering of a wheel in a 'hole'. Meaning it is stuck or falling.
        :param obstacles: to be detected.
        """

        self.left_wheel.set_sensible_obstacles(obstacles)
        self.right_wheel.set_sensible_obstacles(obstacles)
        self.rear_ultrasonic_sensor.set_sensible_obstacles(obstacles)


    def get_sprites(self) -> [Sprite]:
        return self.sprites


    def get_sensors(self) -> [BodyPart]:
        return [self.center_color_sensor,
                self.left_color_sensor,
                self.right_color_sensor,
                self.right_touch_sensor,
                self.left_touch_sensor,
                self.front_ultrasonic_sensor,
                self.rear_ultrasonic_sensor]
