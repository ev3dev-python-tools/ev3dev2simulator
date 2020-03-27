import math

import arcade
import pymunk
from pymunk import PivotJoint, PinJoint, Vec2d

from ev3dev2simulator.obstacle import ColorObstacle
from ev3dev2simulator.robot import BodyPart
from ev3dev2simulator.robot.Arm import Arm
from ev3dev2simulator.robot.Brick import Brick
from ev3dev2simulator.robot.ColorSensor import ColorSensor
from ev3dev2simulator.robot.Led import Led
from ev3dev2simulator.robot.Speaker import Speaker
from ev3dev2simulator.robot.TouchSensor import TouchSensor
from ev3dev2simulator.robot.UltrasonicSensorBottom import UltrasonicSensorBottom
from ev3dev2simulator.robot.UltrasonicSensorTop import UltrasonicSensor
from ev3dev2simulator.robot.Wheel import Wheel
from ev3dev2simulator.util.Util import calc_differential_steering_angle_x_y
from ev3dev2simulator.config.config import get_simulation_settings, debug
from ev3dev2simulator.visualisation.PymunkRobotPartSprite import PymunkRobotPartSprite


class RobotState:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """

    def __init__(self, config):
        self.sprite_list = arcade.SpriteList[PymunkRobotPartSprite]()
        self.side_bar_sprites = arcade.SpriteList()
        self.sensors = {}
        self.actuators = {}
        self.values = {}
        self.led_colors = {}
        self.bricks = []
        self.sounds = {}
        self.joints = []
        self.body = None
        if debug:
            self.debug_shapes = []

        self.orig_x = float(config['center_x'])
        self.orig_y = float(config['center_y']) + 22.5

        self.x = self.orig_x
        self.y = self.orig_y

        try:
            self.orig_orientation = config['orientation']
        except KeyError:
            self.orig_orientation = 0

        sim_settings = get_simulation_settings()
        self.wheel_distance = sim_settings['wheel_settings']['spacing']  # TODO move this to robot config

        self.name = config['name']
        self.is_stuck = False

        for part in config['parts']:
            if part['type'] == 'brick':
                brick = Brick(int(part['brick']), self, float(part['x_offset']), float(part['y_offset']), part['name'])
                self.bricks.append(brick)
                left_led = Led(int(part['brick']), self, float(part['x_offset']) - 20,
                               float(part['y_offset']) - 32.5)
                right_led = Led(int(part['brick']), self, float(part['x_offset']) + 20,
                                float(part['y_offset']) - 32.5)
                self.led_colors[(brick.brick, 'led0')] = 1
                self.actuators[(brick.brick, 'led0')] = left_led
                self.led_colors[(brick.brick, 'led1')] = 1
                self.actuators[(brick.brick, 'led1')] = right_led

                speaker = Speaker(int(part['brick']), self, 0, 0)
                self.actuators[(brick.brick, 'speaker')] = speaker

            elif part['type'] == 'motor':
                wheel = Wheel(int(part['brick']), part['port'], self, float(part['x_offset']), float(part['y_offset']))
                self.actuators[(wheel.brick, wheel.address)] = wheel

            elif part['type'] == 'color_sensor':
                color_sensor = ColorSensor(int(part['brick']), part['port'], self,
                                           float(part['x_offset']),
                                           float(part['y_offset']), part['name'])
                self.sensors[(color_sensor.brick, color_sensor.address)] = color_sensor

            elif part['type'] == 'touch_sensor':
                touch_sensor = TouchSensor(int(part['brick']), part['port'], self, float(part['x_offset']),
                                           float(part['y_offset']), part['side'], part['name'])
                self.sensors[(touch_sensor.brick, touch_sensor.address)] = touch_sensor

            elif part['type'] == 'ultrasonic_sensor':
                try:
                    if part['direction'] == 'bottom':
                        ultrasonic_sensor = UltrasonicSensorBottom(int(part['brick']), part['port'], self,
                                                                   float(part['x_offset']),
                                                                   float(part['y_offset']),
                                                                   part['name'])
                    elif part['direction'] == 'forward':
                        ultrasonic_sensor = UltrasonicSensor(int(part['brick']), part['port'], self,
                                                             float(part['x_offset']),
                                                             float(part['y_offset']),
                                                             part['name'])
                except KeyError:
                    ultrasonic_sensor = UltrasonicSensor(part['brick'], part['port'], self,
                                                         float(part['x_offset']),
                                                         float(part['y_offset']),
                                                         part['name'])
                self.sensors[(ultrasonic_sensor.brick, ultrasonic_sensor.address)] = ultrasonic_sensor
            elif part['type'] == 'arm':
                arm = Arm(int(part['brick']), part['port'], self, float(part['x_offset']),
                          float(part['y_offset']))
                self.side_bar_sprites.append(arm.side_bar_arm)
                self.actuators[(arm.brick, arm.address)] = arm
            else:
                print("Unknown robot part in config")

        self.parts = list(self.sensors.values())
        self.parts.extend(list(self.actuators.values()))
        self.parts.extend(self.bricks)

    def reset(self):
        self.values.clear()
        self._move_x(self.orig_x - self.x)
        self.x = self.orig_x
        self._move_y(self.orig_y - self.y)
        self.y = self.orig_y
        self._rotate(math.radians(self.orig_orientation) - math.radians(self.get_anchor().angle))

    def setup_visuals(self, scale):
        moment = pymunk.moment_for_box(20, (200 * scale, 300 * scale))

        self.body = pymunk.Body(20, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(self.x * scale, self.y * scale)
        shape_filter = pymunk.ShapeFilter(group=1)

        self.scale = scale
        for part in self.parts:
            part.setup_visuals(scale, self.body)
            self.sprite_list.append(part.sprite)
            part.sprite.shape.filter = shape_filter

        if self.orig_orientation != 0:
            self._rotate(math.radians(self.orig_orientation))

    def _move_x(self, distance: float):
        """
        Move all parts of this robot by the given distance in the x-direction.
        :param distance: to move
        """
        self.body.position = self.body.position + (distance * self.scale, 0)

    def _move_y(self, distance: float):
        """
        Move all parts of this robot by the given distance in the y-direction.
        :param distance: to move
        """
        self.body.position = self.body.position + (0, distance * self.scale)

    def _rotate(self, radians: float):
        """
        Rotate all parts of this robot by the given angle in radians.
        :param radians to rotate
        """
        self.body.angle += radians

    def execute_movement(self, left_ppf: float, right_ppf: float):
        """
        Move the robot and its parts by providing the speed of the left and right motor
        using the differential steering principle.
        :param left_ppf: speed in pixels per second of the left motor.
        :param right_ppf: speed in pixels per second of the right motor.
        """

        distance_left = left_ppf if left_ppf is not None else 0
        distance_right = right_ppf if right_ppf is not None else 0

        cur_angle = math.radians(self.get_anchor().sprite.angle + 90)

        diff_angle, diff_x, diff_y = \
            calc_differential_steering_angle_x_y(self.wheel_distance,
                                                 distance_left,
                                                 distance_right,
                                                 cur_angle)

        self.x += diff_x
        self.y += diff_y

        self._rotate(diff_angle)
        self._move_x(diff_x)
        self._move_y(diff_y)

    def execute_arm_movement(self, address: (int, str), dfp: float):
        """
        Move the robot arm by providing the speed of the center motor.
        :param address: the address of the arm
        :param dfp: speed in degrees per second of the center motor.
        """
        self.actuators[address].rotate_arm(dfp)

    def set_led_color(self, address, color):
        self.actuators[address].set_color_texture(color)

    def set_color_obstacles(self, obstacles: [ColorObstacle]):
        """
        Set the obstacles which can be detected by the color sensors of this robot.
        :param obstacles: to be detected.
        """
        for part in self.sensors.values():
            if part.get_ev3type() == 'color_sensor':
                part.set_sensible_obstacles(obstacles)

    def set_touch_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the touch sensors of this robot.
        :param obstacles: to be detected.
        """
        for part in self.sensors.values():
            if part.get_ev3type() == 'touch_sensor':
                part.set_sensible_obstacles(obstacles)

    def set_falling_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the wheel of this robot. This simulates
        the entering of a wheel in a 'hole'. Meaning it is stuck or falling.
        :param obstacles: to be detected.
        """
        for part in self.actuators.values():
            if part.get_ev3type() == 'motor':
                part.set_sensible_obstacles(obstacles)
        for part in self.sensors.values():
            if isinstance(part, UltrasonicSensorBottom):
                part.set_sensible_obstacles(obstacles)

    def get_sensor(self, address):
        return self.sensors.get(address)

    def get_actuators(self):
        return self.actuators.values()

    def get_actuator(self, address):
        return self.actuators[address]

    def get_value(self, address):
        return self.values[address]

    def get_wheels(self):
        wheels = []
        for part in self.actuators.values():
            if part.get_ev3type() == 'motor':
                wheels.append(part)
        return wheels

    def get_sprites(self) -> arcade.SpriteList[PymunkRobotPartSprite]:
        return self.sprite_list

    def get_bricks(self):
        return self.bricks

    def get_sensors(self) -> [BodyPart]:
        return self.sensors.values()

    def get_anchor(self) -> BodyPart:
        if len(self.bricks) != 0:
            return self.bricks[0]
        return None
