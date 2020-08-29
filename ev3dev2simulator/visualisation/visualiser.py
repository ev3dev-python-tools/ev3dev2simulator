"""
The visualiser module handles the timing and the visualisation of the ev3dev2simulator.
Most of the module is contained in the class Visualiser. Creating the class creates a GUI.
"""

import sys
import platform

import arcade as _arcade
import pyglet

from arcade.color import RED

from ev3dev2simulator.state.world_state import WorldState
from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.util.instance_checker import InstanceChecker
from ev3dev2simulator.util.point import Point
from ev3dev2simulator.visualisation.sidebar import Sidebar
from ev3dev2simulator.config.config import get_simulation_settings, DEBUG
from ev3dev2simulator.version import __version__ as sim_version
from ev3dev2.version import __version__ as api_version


class Visualiser(_arcade.Window):
    """
    Main simulator class.
    This class extends from arcade.Window and manages the updates and rendering of the simulator window.
    """

    def __init__(self, update_world_cb, world_state: WorldState, show_fullscreen: bool,
                 show_maximized: bool, use_second_screen_to_show_simulator: bool):

        instance_checker = InstanceChecker(self)
        instance_checker.check_for_unique_instance()

        self.update_callback = update_world_cb
        self.world_state = world_state

        self.current_screen_index = None
        self.set_screen_to_display_simulator_at_startup(use_second_screen_to_show_simulator)

        self.size = Dimensions(get_simulation_settings()['screen_settings']['screen_width'],
                               get_simulation_settings()['screen_settings']['screen_height'])

        self.msg_counter = 0

        screen_title = get_simulation_settings()['screen_settings']['screen_title']
        screen_info = screen_title + f'          version: {sim_version}      ev3dev2 api: {api_version}'

        scale = self.determine_scale(self.size.width, self.size.height)
        if DEBUG:
            print('starting simulation with scaling', scale)
            print('arcade version: ', _arcade.version.VERSION)

        super(Visualiser, self).__init__(self.size.width, self.size.height, screen_info, update_rate=1 / 30,
                                         fullscreen=show_fullscreen,
                                         resizable=True, screen=_arcade.get_screens()[self.current_screen_index])

        icon1 = pyglet.image.load(r'assets/images/body.png')
        self.set_icon(icon1)
        _arcade.set_background_color(get_simulation_settings()['screen_settings']['background_color'])

        self.sidebar = self._setup_sidebar()
        self.world_state.setup_pymunk_shapes(scale)
        self.world_state.setup_visuals(scale)

        if show_maximized:
            self.maximize()

        instance_checker.check_for_activation()

    @staticmethod
    def run():
        """Start the actual visualisation after the window is set up"""
        _arcade.run()

    @property
    def _msg_x(self):
        sidebar_width = get_simulation_settings()['screen_settings']['side_bar_width']
        return (self.size.width - sidebar_width) / 2

    def determine_scale(self, new_screen_width, new_screen_height):
        """Determines the scale between board size and screen size in pixel per mm"""
        sidebar_width = get_simulation_settings()['screen_settings']['side_bar_width']
        width_scale = (new_screen_width - sidebar_width) / self.world_state.board_width
        height_scale = new_screen_height / self.world_state.board_height
        if width_scale <= height_scale:
            scale = width_scale
        else:
            scale = height_scale
        self.size.height = int(scale * self.world_state.board_height)
        self.size.width = sidebar_width + int(scale * self.world_state.board_width)
        return scale

    def _change_scale(self, new_screen_width, new_screen_height):
        scale = self.determine_scale(new_screen_width, new_screen_height)
        self.world_state.rescale(scale)

    def _setup_sidebar(self):
        sidebar_width = get_simulation_settings()['screen_settings']['side_bar_width']
        sidebar = Sidebar(Point(self.size.width - sidebar_width, self.size.height - 70),
                          Dimensions(sidebar_width, self.size.height))
        for robot in self.world_state.get_robots():
            sidebar.init_robot(robot.name, robot.sensors, robot.bricks, robot.side_bar_sprites)

        return sidebar

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        self._change_scale(width, height)
        self.sidebar = self._setup_sidebar()
        super().on_resize(width, height)

    def on_draw(self):
        """
        Render the simulation.
        """

        _arcade.start_render()

        for obstacle_list in self.world_state.static_obstacles:
            for shape in obstacle_list.get_shapes():
                if shape.line_width == 1:
                    shape.draw()
                else:
                    print(shape)
        self.world_state.sprite_list.draw()

        for robot in self.world_state.get_robots():
            robot.get_sprites().draw()

            if DEBUG:
                for sprite in robot.get_sprites():
                    sprite.draw_hit_box(color=RED, line_thickness=5)
                    if robot.debug_shapes is not None:
                        for shape in robot.debug_shapes:
                            shape.draw()
                    robot.debug_shapes.clear()

            if robot.is_falling() and self.msg_counter <= 0:
                self.msg_counter = get_simulation_settings()['exec_settings']['frames_per_second'] * 3

        for robot in self.world_state.get_robots():
            self.sidebar.add_robot_info(robot.name, robot.values, robot.sounds)

        self.sidebar.draw()
        if self.msg_counter > 0:
            self.msg_counter -= 1
            _arcade.draw_text(get_simulation_settings()['screen_settings']['falling_message'], self._msg_x,
                              self.size.height - 100, _arcade.color.RADICAL_RED, 14, anchor_x="center")

    def update(self, delta_time):
        """
        All the logic to move the robot. Collision detection is also performed.
        Callback to WorldSimulator.update is called
        """
        self.update_callback()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.world_state.set_object_at_position_as_selected((x, y))

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.world_state.unselect_object()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        if buttons == _arcade.MOUSE_BUTTON_LEFT:
            self.world_state.move_selected_object(dx, dy)
        if buttons == _arcade.MOUSE_BUTTON_RIGHT:
            self.world_state.rotate_selected_object(dy)

    def on_close(self):
        sys.exit(0)

    def on_key_press(self, symbol: int, modifiers: int):
        """Called whenever a key is pressed. """

        # Quit the simulator
        if symbol == _arcade.key.Q:
            self.on_close()

        # Toggle fullscreen between screens (only works at fullscreen mode)
        elif symbol == _arcade.key.T:
            # User hits T. When at fullscreen, then switch screen used for fullscreen.
            if len(_arcade.get_screens()) == 0:
                return
            if self.fullscreen:
                # to switch screen when in fullscreen we first have to back to normal window, and do fullscreen again
                self._set_full_screen(False)
                # Toggle between first and second screen (other screens are ignored)
                self.toggle_screen_used_for_fullscreen()
                self._set_full_screen(True)

        # Maximize window
        # note: is toggle on macOS, but not on windows
        elif symbol == _arcade.key.M:
            self.maximize()

        # Toggle between Fullscreen and window
        #   keeps viewport coordinates the same   STRETCHED (FULLSCREEN)
        #   Instead of a one-to-one mapping to screen size, we use stretch/squash window to match the constants.
        #   src: http://arcade.academy/examples/full_screen_example.html
        elif symbol == _arcade.key.F:
            self.update_current_screen()
            self._set_full_screen(not self.fullscreen)

    def set_screen_to_display_simulator_at_startup(self, use_second_screen_to_show_simulator):
        """ Set screen to use to display the simulator at startup. For windows this works only in fullscreen mode.

           By default set current screen to show simulator, but if use_second_screen_to_show_simulator==True
           then change screen to other screen.

           On MacOS this works for both fullscreen and none-fullscreen mode.
           On Windows this only works for fullscreen mode. For none-fullscreen always the first screen is used.
        """

        # get current_screen_index
        screens = _arcade.get_screens()
        self.current_screen_index = 1 if use_second_screen_to_show_simulator and len(screens) > 1 else 0

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
        #  for macOS  get_default_screen() is also used to as the screen to draw the window initially
        #  for windows the current screen is used to to draw the window initially,
        #              however the value set by get_default_screen() is used as the screen
        #              where to display the window fullscreen!

        # note:  BUG: dragging window to other screen in macOS messes up view size
        #   for macOS the screen of the mac can have higher pixel ratio (self.get_pixel_ratio())
        #   then the second screen connected. If you drag the window from the mac screen to the
        #   second screen then the windows may be the same size, but the simulator is drawn in only
        #   in the lower left quart of the window.
        #      => we need somehow make drawing of the simulator larger

        # how to view simulator window on second screen when dragging not working?
        #    SOLUTION: just when starting up the simulator set it to open on the second screen,
        #              then it goes well, and you can also open it fullscreen on the second screen
        # see also : https://stackoverflow.com/questions/49302201/highdpi-retina-windows-in-pyglet

    # toggle screen for fullscreen
    # BUG: doesn't work on macOS => see explanation in set_screen_to_display_simulator_at_startup() method
    def toggle_screen_used_for_fullscreen(self):
        """toggles between the first two screens found by arcade"""
        # toggle only between screen 0 and 1 (other screens are ignored)
        self.current_screen_index = (self.current_screen_index + 1) % 2

        # override hidden screen parameter in window
        screens = _arcade.get_screens()
        self._screen = screens[self.current_screen_index]

    def update_current_screen(self):
        """ using the windows position and size we determine on which screen it is currently displayed and make that
            current screen for displaying in fullscreen!!
        """

        screens = _arcade.get_screens()
        if len(screens) == 1:
            return

        top_left_x = self.get_location()[0]
        top_left_y = self.get_location()[1]
        size = self.get_size()
        win_width = size[0]
        win_height = size[1]

        done = False
        locations = [self.get_location(), (top_left_x + win_width, top_left_y), (top_left_x, top_left_y + win_height),
                     (top_left_x + win_width, top_left_y + win_height)]
        for [loc_x, loc_y] in locations:
            if done:
                break
            num = 0
            for screen in screens:
                within_screen_width = screen.x <= loc_x < (screen.x + screen.width)
                within_screen_height = screen.y <= (loc_y < (screen.y + screen.height))
                if within_screen_width and within_screen_height:
                    self.current_screen_index = num
                    done = True
                    break
                num += 1

        # override hidden screen parameter in window
        self._screen = screens[self.current_screen_index]

    def _set_full_screen(self, is_full_screen: bool = True):
        self.set_fullscreen(is_full_screen)

        # Instead of a one-to-one mapping, stretch/squash window to match the
        # constants. This does NOT respect aspect ratio. You'd need to
        # do a bit of math for that.
        # HACK for macOS: without this hack fullscreen on the second screen is shifted downwards in the y direction
        #     By also calling the maximize function te position the fullscreen in second screen is corrected!)
        if platform.system().lower() == "darwin":
            self.maximize()

        width, height = self.get_size()
        self._change_scale(width, height)

    def windows_activate(self):
        """brings window to the foreground on windows machines"""
        # noinspection PyProtectedMember
        # pylint: disable=import-outside-toplevel
        from pyglet.libs.win32 import _user32
        from pyglet.libs.win32.constants import SW_SHOWMINIMIZED, SW_SHOWNORMAL
        _user32.ShowWindow(self._hwnd, SW_SHOWMINIMIZED)
        _user32.ShowWindow(self._hwnd, SW_SHOWNORMAL)
        # pylint: enable=import-outside-toplevel
