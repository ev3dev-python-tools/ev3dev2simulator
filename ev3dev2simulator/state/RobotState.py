import math

import arcade as _arcade
import pymunk
from pymunk.vec2d import Vec2d

from ev3dev2simulator.obstacle import ColorObstacle
from ev3dev2simulator.robotpart import BodyPart
from ev3dev2simulator.robotpart.Arm import Arm
from ev3dev2simulator.robotpart.Brick import Brick
from ev3dev2simulator.robotpart.ColorSensor import ColorSensor
from ev3dev2simulator.robotpart.Led import Led
from ev3dev2simulator.robotpart.Speaker import Speaker
from ev3dev2simulator.robotpart.TouchSensor import TouchSensor
from ev3dev2simulator.robotpart.UltrasonicSensorBottom import UltrasonicSensorBottom
from ev3dev2simulator.robotpart.UltrasonicSensorTop import UltrasonicSensor
from ev3dev2simulator.robotpart.Wheel import Wheel

from ev3dev2simulator.util.util import calc_differential_steering_angle_x_y
from ev3dev2simulator.config.config import debug, get_robot_config

class RobotState:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """

    def __init__(self, config):
        self.sprite_list = _arcade.SpriteList()
        self.side_bar_sprites = _arcade.SpriteList()

        self.sensors = {}
        self.actuators = {}
        self.values = {}
        self.led_colors = {}
        self.bricks = []
        self.sounds = {}

        self.body = None
        self.shapes = []
        self.scale = None

        if debug:
            self.debug_shapes = []

        self.x = float(config['center_x'])
        self.y = float(config['center_y']) + 22.5

        self.wheel_distance = None
        self.last_pos_x = None
        self.last_pos_y = None

        try:
            self.orig_orientation = int(config['orientation'])
        except KeyError:
            self.orig_orientation = 0

        self.name = config['name']
        self.is_stuck = False

        parts = get_robot_config(config['type'])['parts'] if 'type' in config else config['parts']

        for part in parts:
            if part['type'] == 'brick':
                brick = Brick(part, self)
                self.bricks.append(brick)
                self.led_colors[(brick.brick, 'led0')] = 1
                self.actuators[(brick.brick, 'led0')] = Led(part['brick'], self, 'left',
                                                            part['x_offset'], part['y_offset'])
                self.led_colors[(brick.brick, 'led1')] = 1
                self.actuators[(brick.brick, 'led1')] = Led(part['brick'], self, 'right',
                                                            part['x_offset'], part['y_offset'])

                self.actuators[(brick.brick, 'speaker')] = Speaker(int(part['brick']), self, 0, 0)

            elif part['type'] == 'motor':
                wheel = Wheel(part, self)
                self.actuators[(wheel.brick, wheel.address)] = wheel

            elif part['type'] == 'color_sensor':
                color_sensor = ColorSensor(part, self)
                self.sensors[(color_sensor.brick, color_sensor.address)] = color_sensor

            elif part['type'] == 'touch_sensor':
                touch_sensor = TouchSensor(part, self)
                self.sensors[(touch_sensor.brick, touch_sensor.address)] = touch_sensor

            elif part['type'] == 'ultrasonic_sensor':
                direction = part['direction'] if 'direction' in part else 'forward'
                if direction == 'bottom':
                    ultrasonic_sensor = UltrasonicSensorBottom(part, self)
                else:
                    ultrasonic_sensor = UltrasonicSensor(part, self)
                self.sensors[(ultrasonic_sensor.brick, ultrasonic_sensor.address)] = ultrasonic_sensor

            elif part['type'] == 'arm':
                arm = Arm(part, self)
                self.side_bar_sprites.append(arm.side_bar_arm)
                self.actuators[(arm.brick, arm.address)] = arm
            else:
                print("Unknown robot part in config")

        self.parts = []
        self.parts.extend(list(self.get_wheels()))
        self.parts.extend(list(self.sensors.values()))
        self.parts.extend(self.bricks)
        self.parts.extend(filter(lambda act: act.get_ev3type() != 'motor', list(self.actuators.values())))

    def set_last_pos(self, pos):
        self.last_pos_x = pos.x * (1 / self.scale)
        self.last_pos_y = pos.y * (1 / self.scale)

    def reset(self):
        self.values.clear()
        self.body.position = pymunk.Vec2d(self.x * self.scale, self.y * self.scale)
        self.body.angle = math.radians(self.orig_orientation)
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        for obj in self.side_bar_sprites:
            obj.reset()

    def setup_pymunk_shapes(self, scale):
        moment = pymunk.moment_for_box(20, (200 * scale, 300 * scale))

        self.body = pymunk.Body(20, moment)
        if self.last_pos_x and self.last_pos_y:
            self.body.position = pymunk.Vec2d(self.last_pos_x * scale, self.last_pos_y * scale)
        else:
            self.body.position = pymunk.Vec2d(self.x * scale, self.y * scale)

        for part in self.parts:
            part.setup_pymunk_shape(scale, self.body)
            self.shapes.append(part.shape)

        wheels = self.get_wheels()
        if len(wheels) == 2:
            wheel_pos_left = Vec2d(wheels[0].shape.center_of_gravity)
            wheel_pos_right = Vec2d(wheels[1].shape.center_of_gravity)
            self.wheel_distance = wheel_pos_left.get_distance(wheel_pos_right)
        else:
            raise RuntimeError('Currently cannot have anything other than 2 wheels')

        if hasattr(self, 'last_angle'):
            self._rotate(math.radians(self.last_angle))
        elif self.orig_orientation != 0:
            self._rotate(math.radians(self.orig_orientation))

        self.scale = scale

    def setup_visuals(self, scale):
        for part in self.parts:
            part.setup_visuals(scale)
            self.sprite_list.append(part.sprite)

    def _move_position(self, distance: Vec2d):
        """
        Move all parts of this robot by the given distance vector.
        :param distance: to move
        """
        self.body.velocity = distance * 30.0

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

        distance_left = left_ppf * self.scale if left_ppf is not None else 0
        distance_right = right_ppf * self.scale if right_ppf is not None else 0

        cur_angle = self.body.angle + math.radians(90)
        diff_angle, diff_x, diff_y = calc_differential_steering_angle_x_y(self.wheel_distance,
                                                                          distance_left,
                                                                          distance_right, cur_angle)
        self._rotate(diff_angle)
        self._move_position(Vec2d(diff_x, diff_y))

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

    def get_shapes(self):
        return self.shapes

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

    def get_sprites(self) -> _arcade.SpriteList:
        return self.sprite_list

    def get_bricks(self):
        return self.bricks

    def get_sensors(self) -> [BodyPart]:
        return self.sensors.values()

    def get_anchor(self) -> BodyPart:
        if len(self.bricks) != 0:
            return self.bricks[0]
        return None
