"""
The robot state contains the RobotState class that handles the state of robot.
This class can be seen as a snapshot of the robot at some point in time.
"""

import math
import threading

import arcade as _arcade
import pymunk
from pymunk.vec2d import Vec2d

from ev3dev2simulator.obstacle import color_obstacle
from ev3dev2simulator.robotpart import body_part
from ev3dev2simulator.robotpart.arm import Arm
from ev3dev2simulator.robotpart.brick import Brick
from ev3dev2simulator.robotpart.color_sensor import ColorSensor
from ev3dev2simulator.robotpart.led import Led
from ev3dev2simulator.robotpart.speaker import Speaker
from ev3dev2simulator.robotpart.touch_sensor import TouchSensor
from ev3dev2simulator.robotpart.ultrasonic_sensor_bottom import UltrasonicSensorBottom
from ev3dev2simulator.robotpart.ultrasonic_sensor_top import UltrasonicSensor
from ev3dev2simulator.robotpart.wheel import Wheel
from ev3dev2simulator.util.point import Point

from ev3dev2simulator.util.util import calc_differential_steering_angle_x_y
from ev3dev2simulator.config.config import DEBUG, get_robot_config


class RobotState:
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """

    def __init__(self, config):
        self.sprite_list = _arcade.SpriteList()
        self.side_bar_sprites = _arcade.SpriteList()

        self.sensors = {}
        # every frame we show the new sensor values in window
        # so we update sensor values in below field every frame.
        # This field is written(and read) by simulator thread and read by ev3dev thread
        # so the prevent corruption by two threads we have to protect access to this field with a mutex.
        self._sensor_values = {}

        self.actuators = {}

        self.led_colors = {}
        self.bricks = []
        self.sounds = {}
        self.config = config

        self.body = None
        self.scale = None

        if DEBUG:
            self.debug_shapes = []

        self.wheel_distance = None
        self.last_pos = None
        self.last_angle = None

        self.name = config['name']


        self.parts = []

        # when initializing robot next to self.parts also self.sensors and selfs.actuators are initialized
        self._init_robot(config)


        # per sensor a lock because simulator thread writes to it, and ev3dev client reads from it
        self.sensor_locks = {}
        self._init_sensors()


    def _init_robot(self,config):
        """
        Adds the parts from the configuration to the robot.
        """
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

        self.parts.extend(list(self.get_wheels()))  # actuators with ev3type() == 'motor'
        self.parts.extend(list(self.sensors.values()))
        self.parts.extend(self.bricks)
        self.parts.extend(filter(lambda act: act.get_ev3type() != 'motor', list(self.actuators.values())))



    def _init_sensors(self):
        """
        Initialize each sensor with its default value.
        Also create an unique lock per sensor sensor.
        """
        for sensor_address, sensor in self.sensors.items():
            self._sensor_values[sensor_address] = sensor.get_default_value()
            self.sensor_locks[sensor_address] = threading.Lock()

    def update_sensors(self):
        """
        Process the data of the robot sensors by retrieving the data and putting it
        in the robot state.
        """
        for address, sensor in self.sensors.items():
            self.sensor_locks[address].acquire()
            self._sensor_values[address] = sensor.get_latest_value()
            self.sensor_locks[address].release()

    def is_falling(self):
        """
        Check if the robot has fallen of the playing field or is stuck in the
        middle of a lake. If so display a message on the screen.
        """
        wheels = self.get_wheels()
        for wheel in wheels:
            if wheel.is_falling():
                return True
        return False


    def set_last_pos(self, pos):
        """
        Updates the last pos as the given position multiplied by the inverse of the scale.
        """
        self.last_pos = Point(pos.x * (1 / self.scale), pos.y * (1 / self.scale))

    def _get_orig_orientation(self):
        """
        Get the orientation of the robot as specified in the robot configuration file
        """
        try:
            return int(self.config['orientation'])
        except KeyError:
            return 0

    def _get_orig_position(self) -> Point:
        """
        Get the position of the robot as specified in the robot configuration file
        """
        return Point(float(self.config['center_x']), float(self.config['center_y']) + 22.5)

    def reset(self):
        """
        Resets the robot to its original position, and resets the all measurements.
        """
        self.clear_values()
        orig_pos = self._get_orig_position()
        self.body.position = pymunk.Vec2d(orig_pos.x * self.scale, orig_pos.y * self.scale)
        self.body.angle = math.radians(self._get_orig_orientation())
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        for obj in self.side_bar_sprites:
            obj.reset()

    def reset_position(self):
        """
        Resets the robot to its original position and angle ,but
        does not reset its speed because the running robot program expects that speed still set.
        Handy function to continue testing when robot drove off the map, to replace it back on the map.
        """
        #self.clear_values() # hangs simulator => sensor values will be update automatically anyway by program
        orig_pos = self._get_orig_position()
        self.body.position = pymunk.Vec2d(orig_pos.x * self.scale, orig_pos.y * self.scale)
        self.body.angle = math.radians(self._get_orig_orientation())
        #self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        for obj in self.side_bar_sprites:
            obj.reset()

    def setup_pymunk_shapes(self, scale):
        """
        Creates the body of the robot and adds the shapes of all robot parts.
        """
        self.scale = scale
        moment = pymunk.moment_for_box(20, (200 * scale, 300 * scale))

        self.body = pymunk.Body(20, moment)
        if self.last_pos:
            self.body.position = pymunk.Vec2d(self.last_pos.x * scale, self.last_pos.y * scale)
        else:
            orig_pos = self._get_orig_position()
            self.body.position = pymunk.Vec2d(orig_pos.x * scale, orig_pos.y * scale)

        shapes = []
        for part in self.parts:
            part.setup_pymunk_shape(scale, self.body)
            shapes.append(part.shape)

        wheels = self.get_wheels()
        if len(wheels) == 2:
            wheel_pos_left = Vec2d(*wheels[0].shape.center_of_gravity)
            wheel_pos_right = Vec2d(*wheels[1].shape.center_of_gravity)
            self.wheel_distance = wheel_pos_left.get_distance(wheel_pos_right)
        else:
            raise RuntimeError('Currently cannot have anything other than 2 wheels')

        if self.last_angle:
            self._rotate(math.radians(self.last_angle))
        elif self._get_orig_orientation() != 0:
            self._rotate(math.radians(self._get_orig_orientation()))


        return shapes

    def setup_visuals(self, scale):
        """
        Creates the sprite list based on all the parts of the robot.
        """
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

        # update physical properties of rover (its pymunk physical object used in physical simulation)
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
        """
        Sets the led texture of the led behind address to color
        """
        self.actuators[address].set_color_texture(color)

    def set_color_obstacles(self, obstacles: [color_obstacle]):
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

    def get_sensor(self, address):
        """
        Gets the sensor based on its ev3dev address.
        """
        return self.sensors.get(address)

    def get_actuators(self):
        """
         Gets all actuators of the robot in a list.
         """
        return self.actuators.values()

    def get_actuator(self, address):
        """
         Gets an actuator based on its ev3dev address.
         """
        return self.actuators[address]

    def get_value(self, address):
        """
         Gets value of a sensor based on the ev3dev address of the sensor.
         """
        self.sensor_locks[address].acquire()
        value=self._sensor_values[address]
        self.sensor_locks[address].release()
        return value

    def get_values(self):
        """
         Gets values of all sensors
         """

        # creates shallow copy which is fine because values in dict are copy values (no references as values)
        # note: need to loop over dict keys so we can fetch each value with a mutex lock
        values={}
        for address in self._sensor_values.keys():
            values[address] = self.get_value(address)
            self.sensor_locks[address].acquire()
            values[address] = self._sensor_values[address]
            self.sensor_locks[address].release()
        return values

    def set_value(self, address, value):
        """
         Sets value of a sensor based on the ev3dev address of the sensor.
         """
        self.sensor_locks[address].acquire()
        self._sensor_values[address] = value
        self.sensor_locks[address].release()

    def clear_values(self):
        """
         Sets value of a sensor based on the ev3dev address of the sensor.
         """
        for address in self._sensor_values.keys():
            self.sensor_locks[address].acquire()
        self._sensor_values.clear()
        for address in self._sensor_values.keys():
            self.sensor_locks[address].release()

    def get_wheels(self):
        """
        Gets all wheels of the robot.
        """
        wheels = []
        for part in self.actuators.values():
            if part.get_ev3type() == 'motor':
                wheels.append(part)
        return wheels

    def get_sprites(self) -> _arcade.SpriteList:
        """
        Gets the sprite list that has all robot part sprites in it.
        """
        return self.sprite_list

    def get_bricks(self):
        """
        Gets the bricks of the robot
        """
        return self.bricks

    def get_sensors(self) -> [body_part]:
        """
        Gets all sensors of the robot.
        """
        return self.sensors.values()

    def get_anchor(self) -> body_part:
        """
        Get the anchor of the robot, which is the first brick connected.
        """
        if len(self.bricks) != 0:
            return self.bricks[0]
        return None
