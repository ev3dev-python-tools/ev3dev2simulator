"""
This module contains the Sidebar class that is used to display information about the current playing field.
It is displayed to the right of the playing field.
"""
from collections import namedtuple

import arcade as _arcade

from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.util.point import Point


class Sidebar:
    """
    The Sidebar class is used to display information about the playing fields and its objects
    """
    def __init__(self, start_point: Point, dimensions: Dimensions):
        self.start = start_point
        self.dims = dimensions

        Styling = namedtuple('Styling', ['text_size', 'text_spacing', 'left_text_padding', 'text_color'])
        self.styling = Styling(10, 10, 10, _arcade.color.WHITE)

        self.robot_info = {}

        self.sprites_total_height = 0

        self.sprites = _arcade.SpriteList()

    def init_robot(self, name, sensors, bricks, side_bar_sprites):
        """
        Initialized a single robot for the sidebar. Creates the sprite for the arm as seen from above.
        Should be called once when a robot is created.
        """
        for sprite in side_bar_sprites:
            sprite.setup_visuals(self.start.x + self.dims.width/2, self.start.y - self.sprites_total_height,
                                 self.dims.width * 0.7, self.dims.width * 0.7 * 0.5)
            self.sprites_total_height += 110
            self.sprites.append(sprite)
        self.robot_info[name] = {}
        for address, sensor in sensors.items():
            self.robot_info[name][address] = {'name': sensor.name, 'value': None}

        for brick in bricks:
            self.robot_info[name][(brick.brick, 'speaker')] = {'name': f'{brick.name} sound', 'value': None}

    def add_robot_info(self, name, values, sounds):
        """
        Adds the current values of the robot to the sidebar.
        """
        robot = self.robot_info[name]
        for address, value in values.items():
            robot[address]['value'] = value
        for address, sound in sounds.items():
            robot[address]['value'] = sound

    def draw(self):
        """
        draws the sidebar based on the information given by ``add_robot_info``
        """

        for sprite in self.sprites:
            sprite.draw()

        height = self.sprites_total_height

        shortcuts=["left mouse: move object/robot","right mouse: rotate object/robot","q : Quit the simulator","m : Maximize simulator window","f : show simulator Fullscreen (toggle)",
                   "t :Toggle screen in fullscreen mode","    toggle only works at fullscreen mode",
                   "w : reset World (not robots)", "p : reset robots Positions","r : Reset world and robots positions"]

        _arcade.draw_text("interface", self.start.x + self.styling.left_text_padding, self.start.y - height,
                          self.styling.text_color, self.styling.text_size + 2, bold=True)
        for shortcut in shortcuts:
            height += (self.styling.text_size + self.styling.text_spacing)
            _arcade.draw_text(shortcut, self.start.x + 2 * self.styling.left_text_padding,
                                  self.start.y - height, self.styling.text_color, self.styling.text_size)

        height += (self.styling.text_size + self.styling.text_spacing)
        height += (self.styling.text_size + self.styling.text_spacing)
        for robot_name, sensor_dict in self.robot_info.items():
            _arcade.draw_text(robot_name, self.start.x + self.styling.left_text_padding, self.start.y - height,
                              self.styling.text_color, self.styling.text_size + 2, bold=True)
            height += (self.styling.text_size + self.styling.text_spacing)
            for _, sensor in sensor_dict.items():
                value = f"{sensor['value']:.2f}" if isinstance(sensor['value'], float) else str(sensor['value'])
                lines = value.count('\n')
                height += (self.styling.text_size * lines)
                _arcade.draw_text(f"{sensor['name']}: {value}", self.start.x + 2 * self.styling.left_text_padding,
                                  self.start.y - height, self.styling.text_color, self.styling.text_size)
                height += (self.styling.text_size + self.styling.text_spacing)
            height += (self.styling.text_size + self.styling.text_spacing)





