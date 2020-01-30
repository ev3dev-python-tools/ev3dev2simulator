"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""
import pyglet
import argparse
import os
import sys
from typing import Tuple

import arcade
from pymunk import Space

# HACK: need to change dir to Simulator script's directory because resources are loaded relative from this directory
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ServerSocketDouble import ServerSocketDouble
from ev3dev2simulator.connection.ServerSocketSingle import ServerSocketSingle
from ev3dev2simulator.obstacle.Border import Border
from ev3dev2simulator.obstacle.Bottle import Bottle
from ev3dev2simulator.obstacle.Edge import Edge
from ev3dev2simulator.obstacle.Lake import BlueLake, GreenLake, RedLake
from ev3dev2simulator.obstacle.Rock import Rock
from ev3dev2simulator.robot.RobotLarge import RobotLarge
from ev3dev2simulator.robot.RobotSmall import RobotSmall
from ev3dev2simulator.state.RobotState import RobotState
from ev3dev2simulator.util.Util import apply_scaling




import tempfile,time

class Simulator(arcade.Window):


    def __init__(self, robot_state: RobotState, robot_pos: Tuple[int, int, int], show_fullscreen: bool, show_maximized: bool, use_second_screen_to_show_simulator: bool):

        self.check_for_unique_instance()

        self.robot_state = robot_state
        self.init_screen(use_second_screen_to_show_simulator)

        self.scaling_multiplier = get_config().get_scale()
        self.large_sim_type = get_config().is_large_sim_type()
        self.cfg = get_config().get_data()

        self.screen_total_width = int(apply_scaling(self.cfg['screen_settings']['screen_total_width']))
        self.screen_width = int(apply_scaling(self.cfg['screen_settings']['screen_width']))
        self.screen_height = int(apply_scaling(self.cfg['screen_settings']['screen_height']))
        from ev3dev2.version import __version__ as apiversion
        from ev3dev2simulator.version import __version__ as simversion
        screen_title = self.cfg['screen_settings']['screen_title'] + "          version: " + simversion + "      ev3dev2 api: " + apiversion

        self.frames_per_second = self.cfg['exec_settings']['frames_per_second']
        self.falling_msg = self.cfg['screen_settings']['falling_message']
        self.restart_msg = self.cfg['screen_settings']['restart_message']

        super(Simulator, self).__init__(self.screen_total_width, self.screen_height, screen_title, update_rate=1 / 30, resizable=True)

        icon1 = pyglet.image.load(r'assets/images/body.png')
        self.set_icon(icon1)
        arcade.set_background_color(eval(self.cfg['screen_settings']['background_color']))

        self.robot_elements = None
        self.obstacle_elements = None

        self.robot = None
        self.robot_pos = robot_pos

        self.red_lake = None
        self.green_lake = None
        self.blue_lake = None

        self.rock1 = None
        self.rock2 = None
        self.bottle1 = None

        self.border = None
        self.edge = None
        self.ground = None

        self.space = None

        self.center_cs_data = 0
        self.left_cs_data = 0
        self.right_cs_data = 0
        self.left_ts_data = False
        self.right_ts_data = False
        self.front_us_data = -1
        self.rear_us_data = -1

        self.text_x = self.screen_width - apply_scaling(220)
        self.msg_x = self.screen_width / 2
        self.msg_counter = 0

        self.setup()

        if show_fullscreen == True:
            self.toggleFullScreen()

        if show_maximized == True:
            self.maximize()

        self.check_for_activation()

    def init_screen(self,use_second_screen_to_show_simulator):
        # get current_screen_index
        current_screen_index=0
        if use_second_screen_to_show_simulator == True:
            current_screen_index=1
        display = pyglet.canvas.get_display()
        screens= display.get_screens()
        num_screens=len(screens)
        if  num_screens== 1:
            current_screen_index=0
        self.current_screen_index=current_screen_index

        # change screen to show simulator
        # HACK override default screen function to change it.
        # Note: arcade window class doesn't has the screen parameter which pyglet has, so by overriding
        #       the get_default_screen method we can still change the screen parameter.
        def get_default_screen():
            """Get the default screen as specified by the user's operating system preferences."""
            return screens[self.current_screen_index]
        display.get_default_screen=get_default_screen

        # note:
        #  for macos  get_default_screen() is also used to as the screen to draw the window initially
        #  for windows the current screen is used to to draw the window initially,
        #              however the value set by get_default_screen() is used as the screen
        #              where to display the window fullscreen!

        # note:  BUG: dragging window to other screen in macos messes up view size
        #   for Macos the screen of the mac can have higher pixel ratio (self.get_pixel_ratio())
        #   then the second screen connected. If you drag the window from the mac screen to the
        #   second screen then the windows may be the same size, but the simulator is drawn in only
        #   in the lower left quart of the window.
        #      => we need somehow make drawing of the simulator larger

        # how to view simulator window on second screen when dragging not working?
        #    SOLUTION: just when starting up the simulator set it to open on the second screen,
        #              then it goes well, and you can also open it fullscreen on the second screen
        # see also : https://stackoverflow.com/questions/49302201/highdpi-retina-windows-in-pyglet


    def check_for_unique_instance(self):

        tmpdir=tempfile.gettempdir()
        self.pidfile = os.path.join(tmpdir,"ev3dev2simulator.pid")
        #print("pidfile:  " + self.pidfile,file=sys.stderr)

        self.pid = str(os.getpid())
        f=open(self.pidfile, 'w')
        f.write(self.pid)
        f.flush()
        f.close()

        time.sleep(2)

        file=open(self.pidfile, 'r')
        line=file.readline()
        file.close()
        read_pid=line.rstrip()
        #print("in check; pid:  " + self.pid + " ,read_pid:  " + read_pid,file=sys.stderr)
        if read_pid != self.pid:
            # other process already running
            sys.exit()

    def check_for_activation(self):
        from pyglet import clock

        def callback(dt):
            file=open(self.pidfile, 'r')
            line=file.readline()
            file.close()
            read_pid=line.rstrip()
            #print("in callback; pid:  " + self.pid + " ,read_pid:  " + read_pid,file=sys.stderr)
            if read_pid != self.pid:

                # other simulator tries to start running
                # write pid to pidfile to notify this simulator is already running
                f=open(self.pidfile, 'w')
                f.write(self.pid)
                f.close()

                platform= sys.platform.lower()
                if platform.startswith('win'):
                    self.windowsActivate()
                else:
                    self.activate()



        clock.schedule_interval(callback, 1)

    def windowsActivate(self):
        from pyglet.libs.win32 import _user32
        from pyglet.libs.win32.constants import SW_SHOWMINIMIZED,SW_SHOWNORMAL
        _user32.ShowWindow(self._hwnd,SW_SHOWMINIMIZED)
        _user32.ShowWindow(self._hwnd,SW_SHOWNORMAL)

    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.obstacle_elements = arcade.ShapeElementList()

        if self.large_sim_type:
            self.robot = RobotLarge(self.cfg, self.robot_pos[0], self.robot_pos[1], self.robot_pos[2])
        else:
            self.robot = RobotSmall(self.cfg, self.robot_pos[0], self.robot_pos[1], self.robot_pos[2])

        for s in self.robot.get_sprites():
            self.robot_elements.append(s)

        for s in self.robot.get_sensors():
            self.robot_state.load_sensor(s)

        self.blue_lake = BlueLake(self.cfg)
        self.green_lake = GreenLake(self.cfg)
        self.red_lake = RedLake(self.cfg)

        self.obstacle_elements.append(self.blue_lake.shape)
        self.obstacle_elements.append(self.green_lake.shape)
        self.obstacle_elements.append(self.red_lake.shape)

        self.border = Border(self.cfg, eval(self.cfg['obstacle_settings']['border_settings']['border_color']))
        self.edge = Edge(self.cfg)

        for s in self.border.shapes:
            self.obstacle_elements.append(s)

        self.space = Space()

        if self.large_sim_type:
            self.rock1 = Rock(apply_scaling(825), apply_scaling(1050), apply_scaling(150), apply_scaling(60), arcade.color.DARK_GRAY, 10)
            self.rock2 = Rock(apply_scaling(975), apply_scaling(375), apply_scaling(300), apply_scaling(90), arcade.color.DARK_GRAY, 130)

            self.ground = arcade.create_rectangle(apply_scaling(1460), apply_scaling(950), apply_scaling(300), apply_scaling(10),
                                                  arcade.color.BLACK)

            self.obstacle_elements.append(self.rock1.shape)
            self.obstacle_elements.append(self.rock2.shape)
            self.obstacle_elements.append(self.ground)

            touch_obstacles = [self.rock1, self.rock2]
            falling_obstacles = [self.blue_lake.hole, self.green_lake.hole, self.red_lake.hole, self.edge]

            self.space.add(self.rock1.poly)
            self.space.add(self.rock2.poly)

        else:
            self.bottle1 = Bottle(apply_scaling(1000), apply_scaling(300), apply_scaling(40), arcade.color.DARK_OLIVE_GREEN)
            self.obstacle_elements.append(self.bottle1.shape)

            touch_obstacles = [self.bottle1]
            falling_obstacles = [self.edge]

            self.space.add(self.bottle1.poly)

        color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]

        self.robot.set_color_obstacles(color_obstacles)
        self.robot.set_touch_obstacles(touch_obstacles)
        self.robot.set_falling_obstacles(falling_obstacles)


    def on_close(self):
        sys.exit(0)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Quit the simulator
        if key == arcade.key.Q:
            self.on_close()

        # Toggle fullscreen
        if key == arcade.key.T:
            # # User hits T. Switch screen used for fullscreen.
            # switch which screen is used for fullscreen ; Toggle between first and second screen (other screens are ignored)
            self.toggleScreenUsedForFullscreen()

        # Maximize window
        # note: is toggle on macos, but not on windows
        if key == arcade.key.M:
             self.maximize()

        # Fullscreen
        #   keeps viewport coordinates the same   STRETCHED (FULLSCREEN)
        #   Instead of a one-to-one mapping to screen size, we use stretch/squash window to match the constants.
        #   src: http://arcade.academy/examples/full_screen_example.html
        if key == arcade.key.F:
            self.toggleFullScreen()


    #toggle screen for fullscreen
    # BUG: doesn't work on macos => see explaination in init_screen() method
    def toggleScreenUsedForFullscreen(self):
        display = pyglet.canvas.get_display()
        screens= display.get_screens()
        num_screens=len(screens)
        if num_screens== 1:
            return
        # toggle only between screen 0 and 1 (other screens are ignored)
        self.current_screen_index=(self.current_screen_index+1)%2

        # override hidden screen parameter in window
        self._screen=screens[self.current_screen_index]

    def toggleFullScreen(self):
        # User hits 'f' Flip between full and not full screen.
        #self.set_fullscreen(not self.fullscreen,self.screen_width*2, self.screen_height*2)
        self.set_fullscreen(not self.fullscreen)

        # Instead of a one-to-one mapping, stretch/squash window to match the
        # constants. This does NOT respect aspect ratio. You'd need to
        # do a bit of math for that.
        self.set_viewport(0, self.screen_width, 0, self.screen_height)

        # HACK for macos: without this hack fullscreen on the second screen is shifted downwards in the y direction
        #                 By also calling the maximize function te position the fullscreen in second screen is corrected!)
        import platform
        if platform.system() == "darwin":
            self.maximize()


    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)

        #TODO: fix BUG with resize on large field
        #      the resize works perfect with the small field
        #      but with the large field when use set_viewport on then resize also works, BUT we loose the arm.  Same happens when we change window to maximize or fullscreen!
        if not self.large_sim_type:
           self.set_viewport(0, self.screen_width, 0, self.screen_height)



    def on_draw(self):
        """
        Render the simulation. This is done in 30 frames per second.
        """

        arcade.start_render()

        self.obstacle_elements.draw()
        self.robot_elements.draw()

        if self.large_sim_type:
            self._draw_text_large_sim()
        else:
            self._draw_text_small_sim()


    def _draw_text_small_sim(self):
        """
        Draw all the text fields.
        """

        center_cs = 'CS:              ' + str(self.center_cs_data)
        left_ts = 'TS  right:    ' + str(self.right_ts_data)
        right_ts = 'TS  left:       ' + str(self.left_ts_data)
        top_us = 'US:              ' + str(int(round(self.front_us_data / self.scaling_multiplier))) + 'mm'

        message = self.robot_state.next_sound_job()
        sound = message if message else '-'

        arcade.draw_text(center_cs, self.text_x, self.screen_height - apply_scaling(80), arcade.color.BLACK_LEATHER_JACKET, 10)
        arcade.draw_text(left_ts, self.text_x, self.screen_height - apply_scaling(100), arcade.color.BLACK_LEATHER_JACKET, 10)
        arcade.draw_text(right_ts, self.text_x, self.screen_height - apply_scaling(120), arcade.color.BLACK_LEATHER_JACKET, 10)
        arcade.draw_text(top_us, self.text_x, self.screen_height - apply_scaling(140), arcade.color.BLACK_LEATHER_JACKET, 10)
        arcade.draw_text('Sound:', self.text_x, self.screen_height - apply_scaling(160), arcade.color.BLACK_LEATHER_JACKET, 10)
        arcade.draw_text(sound, self.text_x, self.screen_height - apply_scaling(180), arcade.color.BLACK_LEATHER_JACKET, 10, anchor_y='top')

        if self.msg_counter != 0:
            self.msg_counter -= 1

            arcade.draw_text(self.falling_msg, self.msg_x, self.screen_height - apply_scaling(100), arcade.color.BLACK_LEATHER_JACKET, 14,
                             anchor_x="center")
            arcade.draw_text(self.restart_msg, self.msg_x, self.screen_height - apply_scaling(130), arcade.color.BLACK_LEATHER_JACKET, 14,
                             anchor_x="center")


    def _draw_text_large_sim(self):
        """
        Draw all the text fields.
        """

        center_cs = 'CS  ctr:       ' + str(self.center_cs_data)
        left_cs = 'CS  left:      ' + str(self.left_cs_data)
        right_cs = 'CS  right:    ' + str(self.right_cs_data)
        left_ts = 'TS  right:     ' + str(self.right_ts_data)
        right_ts = 'TS  left:        ' + str(self.left_ts_data)
        top_us = 'US  top:       ' + str(int(round(self.front_us_data / self.scaling_multiplier))) + 'mm'
        bottom_us = 'US  bot:       ' + str(int(round(self.rear_us_data))) + 'mm'

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
        if self.large_sim_type:
            self.robot.set_left_brick_led_colors(self.robot_state.left_brick_left_led_color,
                                                 self.robot_state.left_brick_right_led_color)

            self.robot.set_right_brick_led_colors(self.robot_state.right_brick_left_led_color,
                                                  self.robot_state.right_brick_right_led_color)
        else:
            self.robot.set_led_colors(self.robot_state.right_brick_left_led_color,
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
        self.left_ts_data = self.robot.left_touch_sensor.is_touching()
        self.right_ts_data = self.robot.right_touch_sensor.is_touching()
        self.front_us_data = self.robot.front_ultrasonic_sensor.distance(self.space)

        self.robot_state.values[self.robot.center_color_sensor.address] = self.center_cs_data
        self.robot_state.values[self.robot.left_touch_sensor.address] = self.left_ts_data
        self.robot_state.values[self.robot.right_touch_sensor.address] = self.right_ts_data
        self.robot_state.values[self.robot.front_ultrasonic_sensor.address] = self.front_us_data

        self.robot.center_color_sensor.set_color_texture(self.center_cs_data)

        if self.large_sim_type:
            self.left_cs_data = self.robot.left_color_sensor.get_sensed_color()
            self.right_cs_data = self.robot.right_color_sensor.get_sensed_color()
            self.rear_ts_data = self.robot.rear_touch_sensor.is_touching()
            self.rear_us_data = self.robot.rear_ultrasonic_sensor.distance()

            self.robot_state.values[self.robot.left_color_sensor.address] = self.left_cs_data
            self.robot_state.values[self.robot.right_color_sensor.address] = self.right_cs_data
            self.robot_state.values[self.robot.rear_touch_sensor.address] = self.rear_ts_data
            self.robot_state.values[self.robot.rear_ultrasonic_sensor.address] = self.rear_us_data

            self.robot.left_color_sensor.set_color_texture(self.left_cs_data)
            self.robot.right_color_sensor.set_color_texture(self.right_cs_data)


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version",
                        action='store_true',
                        help="Show version info")
    parser.add_argument("-s", "--window_scaling",
                        default=0.65,
                        help="Scaling of the screen, default is 0.65",
                        required=False,
                        type=validate_scale)
    parser.add_argument("-t", "--simulation_type",
                        choices=['small', 'large'],
                        default='small',
                        help="Type of the simulation (small or large). Default is small",
                        required=False,
                        type=str)
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

    parser.add_argument("-2", "--show-on-second-monitor",
                        action='store_true',
                        help="Show simulator window on second monitor instead, default is first monitor")
    parser.add_argument("-f", "--fullscreen",
                        action='store_true',
                        help="Show simulator fullscreen")
    parser.add_argument("-m", "--maximized",
                        action='store_true',
                        help="Show simulator maximized")

    args = vars(parser.parse_args())

    if args['version'] == True:
        from ev3dev2 import version as apiversion
        from ev3dev2simulator import version as simversion
        print("version ev3dev2           : " + apiversion.__version__)
        print("version ev3dev2simulator  : " + simversion.__version__)
        sys.exit(0)

    config = get_config()

    s = args['window_scaling']
    config.write_scale(s)

    t = args['simulation_type']
    config.write_sim_type(t)

    x = apply_scaling(args['robot_position_x'])
    y = apply_scaling(args['robot_position_y'])
    o = args['robot_orientation']

    c = args['connection_order_first']

    use_second_screen_to_show_simulator=args['show_on_second_monitor']
    show_fullscreen=args['fullscreen']
    show_maximized=args['maximized']


    robot_state = RobotState()
    robot_pos = (x, y, o)



    sim = Simulator(robot_state, robot_pos, show_fullscreen, show_maximized, use_second_screen_to_show_simulator)
    #sim.setup()

    server_thread = ServerSocketDouble(robot_state, c) if t == 'large' else ServerSocketSingle(robot_state)
    server_thread.setDaemon(True)
    server_thread.start()

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
