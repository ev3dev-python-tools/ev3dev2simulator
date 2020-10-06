"""
The rock module contains the class Rock, an obstacle on the playground.
"""

import math

import arcade as _arcade
import pymunk
from arcade import Sprite

from ev3dev2simulator.obstacle.movable_object import MovableObject
from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.util.point import Point


class Rock(MovableObject):
    """
    This class represents a 'rock'. Rocks are rectangles.
    """
    def __init__(self,
                 pos: Point,
                 dims: Dimensions,
                 color: _arcade.Color,
                 angle: int,
                 movable: bool):
        super().__init__(pos, angle, color)
        self.movable = movable
        self.new_angle = None
        self.width = dims.width
        self.height = dims.height

    @property
    def cur_angle(self):
        """
        Returns the current orientation of the rock.
        """
        if self.new_angle:
            return self.new_angle
        return self.angle

    def create_shape(self, scale):
        """
        Creates the shape of the rock.
        """
        width = scale * self.width
        height = scale * self.height
        mass = 5
        friction = 0.2
        moment = pymunk.moment_for_box(mass, (width, height))

        self.body = pymunk.Body(mass, moment,
                                body_type=pymunk.Body.DYNAMIC if self.movable is True else pymunk.Body.KINEMATIC)

        pos_x, pos_y = self.get_pos()
        self.body.position = pymunk.Vec2d(pos_x * scale, pos_y * scale)

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.friction = friction
        self.body.angle = math.radians(self.cur_angle)
        self.scale = scale

    def create_sprite(self, scale):
        """
        Create the sprite of the rock based on the scale.
        """
        pos_x, pos_y = self.get_pos()
        self.sprite = Sprite('assets/images/brick.png', scale=scale * (self.width / 892),
                             center_x=pos_x * scale, center_y=pos_y * scale)
        self.sprite.width = scale * self.width
        self.sprite.height = scale * self.height
        self.sprite.color = self.color

    @classmethod
    def from_config(cls, config):
        """
        Creates a rock from a rock configuration file instance
        """
        pos = Point(config['x'], config['y'])
        dims = Dimensions(config['width'], config['height'])
        color = tuple(config['color'])
        angle = config['angle']
        movable = True if 'movable' not in config else config['movable']

        return cls(pos, dims, color, angle, movable)
