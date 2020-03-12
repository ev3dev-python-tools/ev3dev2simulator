import pyglet
import os
import sys
from typing import Tuple

import arcade
from pymunk import Space

# HACK: need to change dir to Simulator script's directory because resources are loaded relative from this directory
from ev3dev2simulator.state import WorldState

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.util.Util import apply_scaling

import tempfile
import time


def start():
    arcade.run()


class Visualiser(arcade.Window):
    """
    Main simulator class.
    This class extends from arcade.Window and manages the updates and rendering of the simulator window.
    """

    def __init__(self, update_world_cb, world_state: WorldState, show_fullscreen: bool,
                 show_maximized: bool, use_second_screen_to_show_simulator: bool):

        self.check_for_unique_instance()

        self.world_state = world_state
        self.set_screen_to_display_simulator_at_startup(use_second_screen_to_show_simulator)

        self.scaling_multiplier = get_config().get_scale()
        self.large_sim_type = get_config().is_large_sim_type()
        self.sim_config = get_config().get_visualisation_config()

        self.screen_total_width = int(apply_scaling(self.sim_config['screen_settings']['screen_total_width']))
        self.screen_width = int(apply_scaling(self.sim_config['screen_settings']['screen_width']))
        self.screen_height = int(apply_scaling(self.sim_config['screen_settings']['screen_height']))
        from ev3dev2.version import __version__ as apiversion
        from ev3dev2simulator.version import __version__ as simversion
        screen_title = self.sim_config['screen_settings'][
                           'screen_title'] + f'          version: {simversion}      ev3dev2 api: {apiversion}'

        self.frames_per_second = self.sim_config['exec_settings']['frames_per_second']
        self.falling_msg = self.sim_config['screen_settings']['falling_message']
        self.restart_msg = self.sim_config['screen_settings']['restart_message']

        super(Visualiser, self).__init__(self.screen_total_width, self.screen_height, screen_title, update_rate=1 / 30,
                                         resizable=True)

        icon1 = pyglet.image.load(r'assets/images/body.png')
        self.set_icon(icon1)
        arcade.set_background_color(eval(self.sim_config['screen_settings']['background_color']))

        self.update_callback = update_world_cb

        self.text_x = self.screen_width - apply_scaling(220)
        self.msg_x = self.screen_width / 2
        self.msg_counter = 0

        self.setup()

        if show_fullscreen:
            self.toggleFullScreenOnCurrentScreen()

        if show_maximized:
            self.maximize()

        self.check_for_activation()

    def get_screens(self):
        display = pyglet.canvas.get_display()
        screens = display.get_screens()
        return screens

    def set_screen_to_display_simulator_at_startup(self, use_second_screen_to_show_simulator):
        """ Set screen to use to display the simulator at startup. For windows this works only in fullscreen mode.

           By default set current screen to show simulator, but if use_second_screen_to_show_simulator==True
           then change screen to other screen.

           On MacOS this works for both fullscreen and none-fullscreen mode.
           On Windows this only works for fullscreen mode. For none-fullscreen always the first screen is used.
        """

        # get current_screen_index
        current_screen_index = 0
        if use_second_screen_to_show_simulator:
            current_screen_index = 1
        screens = self.get_screens()
        for screen in screens: print(screen)
        num_screens = len(screens)
        if num_screens == 1:
            current_screen_index = 0
        self.current_screen_index = current_screen_index

        # change screen to show simulator
        # HACK override default screen function to change it.
        # Note: arcade window class doesn't has the screen parameter which pyglet has, so by overriding
        #       the get_default_screen method we can still change the screen parameter.
        def get_default_screen():
            """Get the default screen as specified by the user's operating system preferences."""
            return screens[self.current_screen_index]

        display = pyglet.canvas.get_display()
        display.get_default_screen = get_default_screen

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
        """ Detect whether an other instance is already running. If so then trigger the
            activation for the other instance and terminate this instance.
        """

        tmpdir = tempfile.gettempdir()
        self.pidfile = os.path.join(tmpdir, "ev3dev2simulator.pid")

        self.pid = str(os.getpid())
        f = open(self.pidfile, 'w')
        f.write(self.pid)
        f.flush()
        f.close()

        time.sleep(2)

        file = open(self.pidfile, 'r')
        line = file.readline()
        file.close()
        read_pid = line.rstrip()
        if read_pid != self.pid:
            # other process already running
            sys.exit()

    def check_for_activation(self):
        """ checks each interval whether the simulator windows must be activated (bring to front)

            note: activation can happen when one tries to start another instance of the simulator,
                  and that instance detects an instance is already running. It then triggers the
                  activation for the other instance and terminates itself.
        """
        from pyglet import clock

        def callback(dt):
            file = open(self.pidfile, 'r')
            line = file.readline()
            file.close()
            read_pid = line.rstrip()
            if read_pid != self.pid:

                # other simulator tries to start running
                # write pid to pidfile to notify this simulator is already running
                f = open(self.pidfile, 'w')
                f.write(self.pid)
                f.close()

                import platform
                if platform.system().lower().startswith('win'):
                    self.windowsActivate()
                else:
                    self.activate()

        clock.schedule_interval(callback, 1)

    def windowsActivate(self):
        from pyglet.libs.win32 import _user32
        from pyglet.libs.win32.constants import SW_SHOWMINIMIZED, SW_SHOWNORMAL
        _user32.ShowWindow(self._hwnd, SW_SHOWMINIMIZED)
        _user32.ShowWindow(self._hwnd, SW_SHOWNORMAL)

    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.obstacle_elements = arcade.ShapeElementList()

    def on_close(self):
        sys.exit(0)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Quit the simulator
        if key == arcade.key.Q:
            self.on_close()

        # Toggle fullscreen between screens (only works at fullscreen mode)
        if key == arcade.key.T:
            # User hits T. When at fullscreen, then switch screen used for fullscreen.
            if self.fullscreen and len(self.get_screens()) > 1:
                # to switch screen when in fullscreen we first have to back to normal window, and do fullscreen again
                self.set_fullscreen(False)
                # switch which screen is used for fullscreen ; Toggle between first and second screen (other screens are ignored)
                self.toggleScreenUsedForFullscreen()
                self.setFullScreen()

        # Maximize window
        # note: is toggle on macos, but not on windows
        if key == arcade.key.M:
            self.maximize()

        # Toggle between Fullscreen and window
        #   keeps viewport coordinates the same   STRETCHED (FULLSCREEN)
        #   Instead of a one-to-one mapping to screen size, we use stretch/squash window to match the constants.
        #   src: http://arcade.academy/examples/full_screen_example.html
        if key == arcade.key.F:
            self.updateCurrentScreen()
            self.toggleFullScreenOnCurrentScreen()

    # toggle screen for fullscreen
    # BUG: doesn't work on macos => see explaination in set_screen_to_display_simulator_at_startup() method
    def toggleScreenUsedForFullscreen(self):

        # toggle only between screen 0 and 1 (other screens are ignored)
        self.current_screen_index = (self.current_screen_index + 1) % 2

        # override hidden screen parameter in window
        screens = self.get_screens()
        self._screen = screens[self.current_screen_index]

    def updateCurrentScreen(self):
        """ using the windows position and size we determine on which screen it is currently displayed and make that
            current screen for displaying in fullscreen!!
        """

        screens = self.get_screens()
        if len(screens) == 1:
            return

        location = self.get_location()
        topleft_x = location[0]
        topleft_y = location[1]
        size = self.get_size()
        win_width = size[0]
        win_height = size[1]

        done = False
        locations = [location, (topleft_x + win_width, topleft_y), (topleft_x, topleft_y + win_height),
                     (topleft_x + win_width, topleft_y + win_height)]
        for location in locations:
            if done:
                break
            loc_x = location[0]
            loc_y = location[1]
            num = 0
            for screen in screens:
                within_screen_width = (loc_x >= screen.x) and (loc_x < (screen.x + screen.width))
                within_screen_height = (loc_y >= screen.y) and (loc_y < (screen.y + screen.height))
                if within_screen_width and within_screen_height:
                    self.current_screen_index = num
                    done = True
                    break
                num = num + 1

        # override hidden screen parameter in window
        self._screen = screens[self.current_screen_index]

    def toggleFullScreenOnCurrentScreen(self):
        # User hits 'f' Flip between full and not full screen.
        self.set_fullscreen(not self.fullscreen)

        # Instead of a one-to-one mapping, stretch/squash window to match the
        # constants. This does NOT respect aspect ratio. You'd need to
        # do a bit of math for that.
        self.set_viewport(0, self.screen_width, 0, self.screen_height)

        # HACK for macos: without this hack fullscreen on the second screen is shifted downwards in the y direction
        #                 By also calling the maximize function te position the fullscreen in second screen is corrected!)
        import platform
        if self.fullscreen and platform.system().lower() == "darwin":
            self.maximize()

    def setFullScreen(self):
        # self.fullscreen=True
        self.set_fullscreen(True)

        # Instead of a one-to-one mapping, stretch/squash window to match the
        # constants. This does NOT respect aspect ratio. You'd need to
        # do a bit of math for that.
        self.set_viewport(0, self.screen_width, 0, self.screen_height)

        # HACK for macos: without this hack fullscreen on the second screen is shifted downwards in the y direction
        #                 By also calling the maximize function te position the fullscreen in second screen is corrected!)
        import platform
        if platform.system().lower() == "darwin":
            self.maximize()

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)

        # TODO: fix BUG with resize on large field
        #      the resize works perfect with the small field
        #      but with the large field when use set_viewport on then resize also works, BUT we loose the arm.  Same happens when we change window to maximize or fullscreen!
        if not self.large_sim_type:
            self.set_viewport(0, self.screen_width, 0, self.screen_height)

    def on_draw(self):
        """
        Render the simulation. This is done in 30 frames per second.
        """
        arcade.start_render()
        for obstacleList in self.world_state.obstacles:
            for shape in obstacleList.get_shapes():
                shape.draw()

        # self.robot_elements.draw()

        self._draw_text()

    def _draw_text(self):
        """
        Draw all the text fields.
        """
        # center_cs = 'CS  ctr:       ' + str(self.center_cs_data)
        # left_cs = 'CS  left:      ' + str(self.left_cs_data)
        # right_cs = 'CS  right:    ' + str(self.right_cs_data)
        # left_ts = 'TS  right:     ' + str(self.right_ts_data)
        # right_ts = 'TS  left:        ' + str(self.left_ts_data)
        # top_us = 'US  top:       ' + str(int(round(self.front_us_data / self.scaling_multiplier))) + 'mm'
        # bottom_us = 'US  bot:       ' + str(int(round(self.rear_us_data))) + 'mm'
        #
        # message = self.robot_state.next_sound_job()
        # sound = message if message else '-'
        #
        arcade.draw_text("testeroni", self.text_x, self.screen_height - apply_scaling(70), arcade.color.BLACK, 10)
        # arcade.draw_text(center_cs, self.text_x, self.screen_height - apply_scaling(70), arcade.color.WHITE, 10)
        # arcade.draw_text(left_cs, self.text_x, self.screen_height - apply_scaling(90), arcade.color.WHITE, 10)
        # arcade.draw_text(right_cs, self.text_x, self.screen_height - apply_scaling(110), arcade.color.WHITE, 10)
        # arcade.draw_text(left_ts, self.text_x, self.screen_height - apply_scaling(130), arcade.color.WHITE, 10)
        # arcade.draw_text(right_ts, self.text_x, self.screen_height - apply_scaling(150), arcade.color.WHITE, 10)
        # arcade.draw_text(top_us, self.text_x, self.screen_height - apply_scaling(170), arcade.color.WHITE, 10)
        # arcade.draw_text(bottom_us, self.text_x, self.screen_height - apply_scaling(190), arcade.color.WHITE, 10)
        # arcade.draw_text('Sound:', self.text_x, self.screen_height - apply_scaling(210), arcade.color.WHITE, 10)
        # arcade.draw_text(sound, self.text_x, self.screen_height - apply_scaling(230), arcade.color.WHITE, 10,
        #                  anchor_y='top')
        #
        # arcade.draw_text('Robot Arm', apply_scaling(1450), self.screen_height - apply_scaling(50), arcade.color.WHITE,
        #                  14,
        #                  anchor_x="center")
        #
        # if self.msg_counter != 0:
        #     self.msg_counter -= 1
        #
        #     arcade.draw_text(self.falling_msg, self.msg_x, self.screen_height - apply_scaling(100), arcade.color.WHITE,
        #                      14,
        #                      anchor_x="center")
        #     arcade.draw_text(self.restart_msg, self.msg_x, self.screen_height - apply_scaling(130), arcade.color.WHITE,
        #                      14,
        #                      anchor_x="center")

    def update(self, delta_time):
        """
        All the logic to move the robot. Collision detection is also performed.
        """
        self.update_callback()

