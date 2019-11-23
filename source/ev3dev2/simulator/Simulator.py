"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""
import argparse
import os
import sys
from typing import Tuple

import arcade
from pymunk import Space

script_dir = os.path.dirname(os.path.realpath(__file__))
ev3dev_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, ev3dev_dir)

os.chdir(script_dir)

from ev3dev2.simulator.config.config import load_config, write_scale_config, load_scale_config
from ev3dev2.simulator.connection.ServerSocket import ServerSocket
from ev3dev2.simulator.obstacle.Border import Border
from ev3dev2.simulator.obstacle.Edge import Edge
from ev3dev2.simulator.obstacle.Lake import BlueLake, GreenLake, RedLake
from ev3dev2.simulator.obstacle.Rock import Rock
from ev3dev2.simulator.robot.Robot import Robot
from ev3dev2.simulator.state.RobotState import get_robot_state, RobotState
from ev3dev2.simulator.util.Util import apply_scaling


class Simulator(arcade.Window):

    def __init__(self, robot_state: RobotState, robot_pos: Tuple[int, int, int]):
        self.cfg = load_config()
        self.robot_state = robot_state

        self.scaling_multiplier = load_scale_config()

        self.screen_total_width = int(apply_scaling(self.cfg['screen_settings']['screen_total_width']))
        self.screen_width = int(apply_scaling(self.cfg['screen_settings']['screen_width']))
        self.screen_height = int(apply_scaling(self.cfg['screen_settings']['screen_height']))
        screen_title = self.cfg['screen_settings']['screen_title']

        self.frames_per_second = self.cfg['exec_settings']['frames_per_second']
        self.falling_msg = self.cfg['screen_settings']['falling_message']
        self.restart_msg = self.cfg['screen_settings']['restart_message']

        super(Simulator, self).__init__(self.screen_total_width, self.screen_height, screen_title, update_rate=1 / 30)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.robot_elements = None
        self.obstacle_elements = None

        self.robot = None
        self.robot_pos = robot_pos

        self.red_lake = None
        self.green_lake = None
        self.blue_lake = None

        self.rock1 = None
        self.rock2 = None

        self.border = None
        self.edge = None
        self.ground = None

        self.space = None

        self.center_cs_data = 0
        self.left_cs_data = 0
        self.right_cs_data = 0
        self.left_ts_data = False
        self.right_ts_data = False
        self.top_us_data = -1
        self.bottom_us_data = -1

        self.text_x = self.screen_width - apply_scaling(220)
        self.msg_x = self.screen_width / 2
        self.msg_counter = 0


    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.obstacle_elements = arcade.ShapeElementList()

        self.robot = Robot(self.cfg, self.robot_pos[0], self.robot_pos[1], self.robot_pos[2])

        for s in self.robot.get_sprites():
            self.robot_elements.append(s)

        for s in self.robot.get_sensors():
            self.robot_state.load_sensor(s)

        self.blue_lake = BlueLake(self.cfg)
        self.green_lake = GreenLake(self.cfg)
        self.red_lake = RedLake(self.cfg)

        self.rock1 = Rock(apply_scaling(825), apply_scaling(1050), apply_scaling(150), apply_scaling(60), arcade.color.DARK_GRAY, 10)
        self.rock2 = Rock(apply_scaling(975), apply_scaling(375), apply_scaling(300), apply_scaling(90), arcade.color.DARK_GRAY, 130)

        self.obstacle_elements.append(self.blue_lake.shape)
        self.obstacle_elements.append(self.green_lake.shape)
        self.obstacle_elements.append(self.red_lake.shape)

        self.obstacle_elements.append(self.rock1.shape)
        self.obstacle_elements.append(self.rock2.shape)

        self.border = Border(self.cfg, arcade.color.WHITE)
        self.edge = Edge(self.cfg)
        self.ground = arcade.create_rectangle(apply_scaling(1460), apply_scaling(950), apply_scaling(300), apply_scaling(10),
                                              arcade.color.BLACK)

        for s in self.border.shapes:
            self.obstacle_elements.append(s)

        self.obstacle_elements.append(self.ground)

        color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]
        touch_obstacles = [self.rock1, self.rock2]
        falling_obstacles = [self.blue_lake.hole, self.green_lake.hole, self.red_lake.hole, self.edge]

        self.robot.set_color_obstacles(color_obstacles)
        self.robot.set_touch_obstacles(touch_obstacles)
        self.robot.set_falling_obstacles(falling_obstacles)

        self.space = Space()
        self.space.add(self.rock1.poly)
        self.space.add(self.rock2.poly)


    def on_draw(self):
        """
        Render the simulation. This is done in 30 frames per second.
        """

        arcade.start_render()

        self.obstacle_elements.draw()
        self.robot_elements.draw()

        self._draw_text()


    def _draw_text(self):
        """
        Draw all the text fields.
        """

        center_cs = 'CS  ctr:       ' + str(self.center_cs_data)
        left_cs = 'CS  left:      ' + str(self.left_cs_data)
        right_cs = 'CS  right:    ' + str(self.right_cs_data)
        left_ts = 'TS  right:     ' + str(self.right_ts_data)
        right_ts = 'TS  left:        ' + str(self.left_ts_data)
        top_us = 'US  top:       ' + str(int(round(self.top_us_data / self.scaling_multiplier))) + 'mm'
        bottom_us = 'US  bot:       ' + str(int(round(self.bottom_us_data))) + 'mm'

        message = self.robot_state.next_sound_job()
        sound = message if message else '-'

        arcade.draw_text(center_cs, self.text_x, self.screen_height - apply_scaling(70), arcade.color.WHITE, 10)
        arcade.draw_text(left_cs, self.text_x, self.screen_height - apply_scaling(90), arcade.color.WHITE, 10)
        arcade.draw_text(right_cs, self.text_x, self.screen_height - apply_scaling(110), arcade.color.WHITE, 10)
        arcade.draw_text(left_ts, self.text_x, self.screen_height - apply_scaling(130), arcade.color.WHITE, 10)
        arcade.draw_text(right_ts, self.text_x, self.screen_height - apply_scaling(150), arcade.color.WHITE, 10)
        arcade.draw_text(top_us, self.text_x, self.screen_height - apply_scaling(170), arcade.color.WHITE, 10)
        arcade.draw_text(bottom_us, self.text_x, self.screen_height - apply_scaling(190), arcade.color.WHITE, 10)
        arcade.draw_text('Sound:', self.text_x, self.screen_height - apply_scaling(210), arcade.color.WHITE, 10)
        arcade.draw_text(sound, self.text_x, self.screen_height - apply_scaling(230), arcade.color.WHITE, 10, anchor_y='top')

        arcade.draw_text('Robot Arm', apply_scaling(1450), self.screen_height - apply_scaling(50), arcade.color.WHITE, 14,
                         anchor_x="center")

        if self.msg_counter != 0:
            self.msg_counter -= 1

            arcade.draw_text(self.falling_msg, self.msg_x, self.screen_height - apply_scaling(100), arcade.color.WHITE, 14,
                             anchor_x="center")
            arcade.draw_text(self.restart_msg, self.msg_x, self.screen_height - apply_scaling(130), arcade.color.WHITE, 14,
                             anchor_x="center")


    def update(self, delta_time):
        """
        All the logic to move the robot. Collision detection is also performed.
        """

        if self.robot_state.should_reset:
            self.setup()
            self.robot_state.reset()

        else:
            self._process_movement()
            self._process_leds()
            self._process_sensors()
            self._check_fall()

        self.robot_state.release_locks()


    def _process_movement(self):
        """
        Request the movement of the robot motors form the robot state and move
        the robot accordingly.
        """

        center_dpf, left_ppf, right_ppf = self.robot_state.next_motor_jobs()

        if left_ppf or right_ppf:
            self.robot.execute_movement(left_ppf, right_ppf)

        if center_dpf:
            self.robot.execute_arm_movement(center_dpf)


    def _process_leds(self):
        self.robot.set_left_brick_led_colors(self.robot_state.left_brick_left_led_color,
                                             self.robot_state.left_brick_right_led_color)

        self.robot.set_right_brick_led_colors(self.robot_state.right_brick_left_led_color,
                                              self.robot_state.right_brick_right_led_color)


    def _check_fall(self):
        """
        Check if the robot has fallen of the playing field or is stuck in the
        middle of a lake. If so display a message on the screen.
        """

        left_wheel_data = self.robot.left_wheel.is_falling()
        right_wheel_data = self.robot.right_wheel.is_falling()

        if left_wheel_data or right_wheel_data:
            self.msg_counter = self.frames_per_second * 3


    def _process_sensors(self):
        """
        Process the data of the robot sensors by retrieving the data and putting it
        in the robot state.
        """

        self.center_cs_data = self.robot.center_color_sensor.get_sensed_color()
        self.left_cs_data = self.robot.left_color_sensor.get_sensed_color()
        self.right_cs_data = self.robot.right_color_sensor.get_sensed_color()
        self.left_ts_data = self.robot.left_touch_sensor.is_touching()
        self.right_ts_data = self.robot.right_touch_sensor.is_touching()
        self.rear_ts_data = self.robot.rear_touch_sensor.is_touching()
        self.top_us_data = self.robot.front_ultrasonic_sensor.distance(self.space)
        self.bottom_us_data = self.robot.rear_ultrasonic_sensor.distance()

        self.robot_state.values[self.robot.center_color_sensor.address] = self.center_cs_data
        self.robot_state.values[self.robot.left_color_sensor.address] = self.left_cs_data
        self.robot_state.values[self.robot.right_color_sensor.address] = self.right_cs_data
        self.robot_state.values[self.robot.left_touch_sensor.address] = self.left_ts_data
        self.robot_state.values[self.robot.right_touch_sensor.address] = self.right_ts_data
        self.robot_state.values[self.robot.rear_touch_sensor.address] = self.rear_ts_data
        self.robot_state.values[self.robot.front_ultrasonic_sensor.address] = self.top_us_data
        self.robot_state.values[self.robot.rear_ultrasonic_sensor.address] = self.bottom_us_data

        self.robot.center_color_sensor.set_color_texture(self.center_cs_data)
        self.robot.left_color_sensor.set_color_texture(self.left_cs_data)
        self.robot.right_color_sensor.set_color_texture(self.right_cs_data)


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--window_scaling",
                        default=load_config()['screen_settings']['scaling_multiplier'],
                        help="Scaling of the screen, default is 0.65",
                        required=False,
                        type=validate_scale)
    parser.add_argument("-x", "--robot_position_x",
                        default=200,
                        help="Starting position x-coordinate of the robot, default is 200",
                        required=False,
                        type=validate_xy)
    parser.add_argument("-y", "--robot_position_y",
                        default=300,
                        help="Starting position y-coordinate of the robot, default is 300",
                        required=False,
                        type=validate_xy)
    parser.add_argument("-o", "--robot_orientation",
                        default=0,
                        help="Starting orientation the robot, default is 0",
                        required=False,
                        type=int)
    parser.add_argument("-c", "--connection_order_first",
                        choices=['left', 'right'],
                        default='left',
                        help="Side of the first brick to connect to the simulator, default is 'left'",
                        required=False,
                        type=str)

    args = vars(parser.parse_args())

    s = args['window_scaling']
    write_scale_config(s)

    x = apply_scaling(args['robot_position_x'])
    y = apply_scaling(args['robot_position_y'])
    o = args['robot_orientation']

    c = args['connection_order_first']

    robot_state = get_robot_state()

    server_thread = ServerSocket(robot_state, c)
    server_thread.setDaemon(True)
    server_thread.start()

    sim = Simulator(robot_state, (x, y, o))
    sim.setup()
    arcade.run()


def validate_scale(value):
    """
    Check if the given value is a valid scale value. Throw an Error if this is not the case.
    :param value: to validate.
    :return: a boolean value representing if the validation was successful.
    """

    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Scaling value must be a floating point number')

    if f < 0.0 or f > 1.0:
        raise argparse.ArgumentTypeError("%s is an invalid scaling value. Should be between 0 and 1" % f)

    return f


def validate_xy(value):
    """
    Check if the given value is a valid xy value. Throw an Error if this is not the case.
    :param value: to validate.
    :return: a boolean value representing if the validation was successful.
    """

    try:
        f = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Coordinate value must be a integer')

    if f < 0 or f > 1000:
        raise argparse.ArgumentTypeError("%s is an invalid coordinate. Should be between 0 and 1000" % f)

    return f


main()
