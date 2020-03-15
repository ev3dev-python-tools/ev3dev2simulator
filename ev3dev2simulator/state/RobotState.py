import math

from arcade import Sprite, arcade
from pymunk import Space

from ev3dev2simulator.obstacle import ColorObstacle
from ev3dev2simulator.robot import BodyPart
from ev3dev2simulator.robot.Arm import Arm
from ev3dev2simulator.robot.ArmLarge import ArmLarge
from ev3dev2simulator.robot.Brick import Brick
from ev3dev2simulator.robot.ColorSensor import ColorSensor
from ev3dev2simulator.robot.Led import Led
from ev3dev2simulator.robot.TouchSensor import TouchSensor
from ev3dev2simulator.robot.UltrasonicSensorBottom import UltrasonicSensorBottom
from ev3dev2simulator.robot.UltrasonicSensorTop import UltrasonicSensor
from ev3dev2simulator.robot.Wheel import Wheel
from ev3dev2simulator.util.Util import calc_differential_steering_angle_x_y, apply_scaling
from ev3dev2simulator.config.config import get_config


class RobotState:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """

    def __init__(self, config):
        self.sprites = arcade.SpriteList()
        self.movable_sprites = arcade.SpriteList()
        self.sensors = {}
        self.actuators = {}
        self.values = {}
        self.led_colors = {}
        self.space = Space()

        self.wheel_center_x = config['center_x']
        self.wheel_center_y = config['center_y'] + apply_scaling(22.5)

        vis_conf = get_config().get_visualisation_config()
        self.wheel_distance = apply_scaling(vis_conf['wheel_settings']['spacing'])  # TODO move this to robot config

        self.name = config['name']

        for part in config['parts']:
            if part['type'] == 'brick':
                brick = Brick(part['brick'], self, part['x_offset'], part['y_offset'], part['name'])
                self.movable_sprites.append(brick)

                left_led = Led(part['brick'], self, apply_scaling(part['x_offset'] - 20),
                               apply_scaling(part['y_offset'] - 32.5))
                right_led = Led(part['brick'], self, apply_scaling(part['x_offset'] + 20),
                                apply_scaling(part['y_offset'] - 32.5))
                self.movable_sprites.append(left_led)
                self.movable_sprites.append(right_led)

                self.led_colors[(brick.brick, 'led0')] = 1
                self.actuators[(brick.brick, 'led0')] = left_led
                self.led_colors[(brick.brick, 'led1')] = 1
                self.actuators[(brick.brick, 'led1')] = right_led

            elif part['type'] == 'motor':
                wheel = Wheel(part['brick'], part['port'], self, apply_scaling(part['x_offset']), part['y_offset'])
                self.movable_sprites.append(wheel)
                self.actuators[(wheel.brick, wheel.address)] = wheel

            elif part['type'] == 'color_sensor':
                color_sensor = ColorSensor(part['brick'], part['port'], self,
                                           apply_scaling(part['x_offset']), apply_scaling(part['y_offset']))
                self.movable_sprites.append(color_sensor)
                self.sensors[(color_sensor.brick, color_sensor.address)] = color_sensor

            elif part['type'] == 'touch_sensor':
                touch_sensor = TouchSensor(part['brick'], part['port'], self, apply_scaling(part['x_offset']),
                                           apply_scaling(part['y_offset']), part['side'])
                self.movable_sprites.append(touch_sensor)
                self.sensors[(touch_sensor.brick, touch_sensor.address)] = touch_sensor

            elif part['type'] == 'ultrasonic_sensor':
                try:
                    if part['direction'] == 'bottom':
                        ultrasonic_sensor = UltrasonicSensorBottom(part['brick'], part['port'], self,
                                                                   apply_scaling(part['x_offset']),
                                                                   apply_scaling(part['y_offset']))
                    elif part['direction'] == 'forward':
                        ultrasonic_sensor = UltrasonicSensor(part['brick'], part['port'], self,
                                                             apply_scaling(part['x_offset']),
                                                             apply_scaling(part['y_offset']))
                except KeyError:
                    ultrasonic_sensor = UltrasonicSensor(part['brick'], part['port'], self,
                                                         apply_scaling(part['x_offset']),
                                                         apply_scaling(part['y_offset']))
                self.movable_sprites.append(ultrasonic_sensor)
                self.sensors[(ultrasonic_sensor.brick, ultrasonic_sensor.address)] = ultrasonic_sensor
            elif part['type'] == 'arm':
                # TODO unused address in part
                arm = Arm(part['brick'], part['port'], self, apply_scaling(part['x_offset']),
                          apply_scaling(part['y_offset']))
                self.movable_sprites.append(arm)
                arm_large = ArmLarge(apply_scaling(1450), apply_scaling(1100))  # TODO this should be automatic
                self.sprites.append(arm_large)
                self.actuators[(arm.brick, arm.address)] = arm
            else:
                print("Unknown robot part in config")

        for sprite in self.movable_sprites:
            self.sprites.append(sprite)

        # for s in self.robot.get_sensors():
        #     self.robot_state.load_sensor(s)

        try:
            orientation = config['orientation']
            if orientation != 0:
                self._rotate(math.radians(orientation))
        except KeyError:
            pass

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

        cur_angle = math.radians(self.get_anchor().angle + 90)

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

    def execute_arm_movement(self, address: (int, str), dfp: float):
        """
        Move the robot arm by providing the speed of the center motor.
        :param address: the address of the arm
        :param dfp: speed in degrees per second of the center motor.
        """

        self.actuators[address].rotate(dfp)

    def set_led_color(self, address, color):
        self.actuators[address].set_color_texture(color)

    def set_space_obstacles(self, obstacles):
        for obstacle in obstacles:
            self.space.add(obstacle.poly)

    def set_color_obstacles(self, obstacles: [ColorObstacle]):
        """
        Set the obstacles which can be detected by the color sensors of this robot.
        :param obstacles: to be detected.
        """
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == 'color_sensor':
                    part.set_sensible_obstacles(obstacles)
            except RuntimeError:
                pass

    def set_touch_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the touch sensors of this robot.
        :param obstacles: to be detected.
        """
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == 'touch_sensor':
                    part.set_sensible_obstacles(obstacles)
            except RuntimeError:
                pass

    def set_falling_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the wheel of this robot. This simulates
        the entering of a wheel in a 'hole'. Meaning it is stuck or falling.
        :param obstacles: to be detected.
        """
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == 'motor':
                    part.set_sensible_obstacles(obstacles)
            except RuntimeError:
                pass

    def get_sensor(self, address):
        return self.sensors.get(address)

    def get_actuators(self):
        return self.actuators.values()

    def get_actuator(self, address):
        print('getting actuator with address', address)
        return self.actuators[address]

    def get_value(self, address):
        return self.values[address]

    def get_wheels(self):
        wheels = []
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == 'motor':
                    wheels.append(part)
            except RuntimeError:
                pass
        return wheels

    def get_sprites(self) -> [Sprite]:
        return self.sprites

    def get_parts_of_type(self, part_type: str):
        sensors = []
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == part_type:
                    sensors.append(part)
            except RuntimeError:
                pass
        return sensors

    def get_sensors(self) -> [BodyPart]:
        sensors = []
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() in ['color_sensor', 'touch_sensor', 'ultrasonic_sensor']:
                    sensors.append(part)
            except RuntimeError:
                pass
        return sensors

    def get_anchor(self) -> BodyPart:
        for part in self.movable_sprites:
            try:
                if part.get_ev3type() == 'brick':
                    return part
            except RuntimeError:
                pass
        return None
