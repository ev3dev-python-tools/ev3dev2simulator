"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""
import argparse

import arcade
from pymunk import Space

from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.ServerSocket import ServerSocket
from ev3dev2.simulator.obstacle.Border import Border
from ev3dev2.simulator.obstacle.Lake import BlueLake, GreenLake, RedLake
from ev3dev2.simulator.obstacle.Rock import Rock
from ev3dev2.simulator.robot.Robot import Robot
from ev3dev2.simulator.state.RobotState import get_robot_state
from ev3dev2.simulator.util.Util import apply_scaling


class Simulator(arcade.Window):

    def __init__(self, robot_state, robot_pos):
        self.cfg = load_config()
        self.robot_state = robot_state

        self.screen_width = apply_scaling(self.cfg['screen_settings']['screen_width'])
        self.screen_height = apply_scaling(self.cfg['screen_settings']['screen_height'])
        screen_title = self.cfg['screen_settings']['screen_title']

        super(Simulator, self).__init__(self.screen_width, self.screen_height, screen_title, update_rate=1 / 30)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.robot_elements = None
        self.obstacle_elements = None

        self.robot = None
        self.robot_start_x = robot_pos[0]
        self.robot_start_y = robot_pos[1]

        self.red_lake = None
        self.green_lake = None
        self.blue_lake = None

        self.rock1 = None
        self.rock2 = None

        self.border = None

        self.space = None

        self.center_cs_data = 0
        self.left_ts_data = False
        self.right_ts_data = False
        self.top_us_data = -1


    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.obstacle_elements = arcade.ShapeElementList()

        self.robot = Robot(self.cfg, self.robot_start_x, self.robot_start_y)

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

        for s in self.border.shapes:
            self.obstacle_elements.append(s)

        color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]
        touch_obstacles = [self.rock1, self.rock2]

        self.robot.set_color_obstacles(color_obstacles)
        self.robot.set_touch_obstacles(touch_obstacles)

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
        center_cs = 'CS center:  ' + str(self.center_cs_data)
        left_ts = 'TS right:      ' + str(self.right_ts_data)
        right_ts = 'TS left:         ' + str(self.left_ts_data)
        top_us = 'US top:        ' + str(int(round(self.top_us_data))) + 'pix'

        message = self.robot_state.next_sound_job()
        sound = message if message else '-'

        arcade.draw_text(center_cs, self.screen_width - 125, self.screen_height - 45, arcade.color.WHITE, 10)
        arcade.draw_text(left_ts, self.screen_width - 125, self.screen_height - 60, arcade.color.WHITE, 10)
        arcade.draw_text(right_ts, self.screen_width - 125, self.screen_height - 75, arcade.color.WHITE, 10)
        arcade.draw_text(top_us, self.screen_width - 125, self.screen_height - 90, arcade.color.WHITE, 10)
        arcade.draw_text('Sound:', self.screen_width - 125, self.screen_height - 105, arcade.color.WHITE, 10)
        arcade.draw_text(sound, self.screen_width - 125, self.screen_height - 120, arcade.color.WHITE, 10,
                         anchor_y='top')


    def update(self, delta_time):
        """
        All the logic to move the robot. Collision detection is also performed.
        """

        if self.robot_state.should_reset:
            self.setup()
            self.robot_state.reset()

        else:
            left_ppf, right_ppf = self.robot_state.next_move_jobs()

            if left_ppf or right_ppf:
                self.robot.execute_movement(left_ppf, right_ppf)

            address_center_cs = self.robot.center_color_sensor.address
            address_left_ts = self.robot.left_touch_sensor.address
            address_right_ts = self.robot.right_touch_sensor.address
            address_us = self.robot.ultrasonic_sensor.address

            self.center_cs_data = self.robot.center_color_sensor.get_sensed_color()
            self.left_ts_data = self.robot.left_touch_sensor.is_touching()
            self.right_ts_data = self.robot.right_touch_sensor.is_touching()
            self.top_us_data = self.robot.ultrasonic_sensor.distance(self.space)

            self.robot_state.values[address_center_cs] = self.center_cs_data
            self.robot_state.values[address_left_ts] = self.left_ts_data
            self.robot_state.values[address_right_ts] = self.right_ts_data
            self.robot_state.values[address_us] = self.top_us_data

        self.robot_state.release_locks()


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-x", "--robot_position_x",
                    help="Starting position x-coordinate of the robot, default is 450",
                    required=False,
                    type=int)
    ap.add_argument("-y", "--robot_position_y",
                    help="Starting position y-coordinate of the robot, default is 600",
                    required=False,
                    type=int)
    # ap.add_argument("-s", "--window_scaling",
    #                 default=load_config()['screen_settings']['scaling_multiplier'],
    #                 help="Scaling of the screen, default is 0.6",
    #                 required=False,
    #                 type=check_scale)

    args = vars(ap.parse_args())
    # lel(args['window_scaling'])

    x = args['robot_position_x'] if args['robot_position_x'] else apply_scaling(450)
    y = args['robot_position_y'] if args['robot_position_y'] else apply_scaling(600)

    robot_state = get_robot_state()

    server_thread = ServerSocket(robot_state)
    server_thread.setDaemon(True)
    server_thread.start()

    sim = Simulator(robot_state, (x, y))
    sim.setup()
    arcade.run()


def check_scale(value):
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Scaling value must be a floating point number')

    if f < 0.0 or f > 1.0:
        raise argparse.ArgumentTypeError("%s is an invalid scaling value. Should be between 0 and 1" % f)

    return f


main()
