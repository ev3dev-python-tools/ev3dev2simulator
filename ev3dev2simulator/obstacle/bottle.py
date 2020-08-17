"""
The module bottle contains the class Bottle, that represents a wine bottle.
"""

import pymunk
import arcade as _arcade
from arcade import Sprite

from ev3dev2simulator.obstacle.movable_object import MovableObject
from ev3dev2simulator.util.point import Point


class Bottle(MovableObject):
    """
    This class represents a 'bottle'. Bottles are circles.
    """
    def __init__(self,
                 pos: Point,
                 radius: float,
                 color: _arcade.Color):
        super().__init__(pos, 0, color)

        self.radius = radius

    @classmethod
    def from_config(cls, config):
        """
        Creates a bottle object from a config dictionary.
        """
        pos = Point(config['x'], config['y'])
        radius = config['radius']
        color = config['color']

        return cls(pos, radius, color)

    def create_shape(self, scale):
        """
        Creates the bottle shape.
        """
        radius = scale * self.radius
        mass = 5
        friction = 0.2
        moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        self.body = pymunk.Body(mass, moment)
        pos_x, pos_y = self.get_pos()
        self.body.position = pymunk.Vec2d(pos_x * scale, pos_y * scale)

        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = friction
        self.scale = scale

    def create_sprite(self, scale):
        """
        Create the sprite, the visuals of the bottle.
        """
        pos_x, pos_y = self.get_pos()
        self.sprite = Sprite('assets/images/bottle.png', scale=scale * 2 * (self.radius / 948),
                             center_x=pos_x * scale, center_y=pos_y * scale)
