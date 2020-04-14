import math

import arcade
import pymunk

from ev3dev2simulator.visualisation.PymunkQuadrilateralSprite import PymunkQuadrilateralSprite


class Rock:
    """
    This class represents a 'rock'. Rocks are rectangles.
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: arcade.Color,
                 angle: int):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

        # visualisation
        self.color = color
        self.sprite = None
        self.scale = None

    def create_sprite(self, scale):
        self.sprite = PymunkQuadrilateralSprite('assets/images/brick.png',
                                                self.x * scale, self.y * scale, scale * (self.width / 892))
        self.sprite.body.angle = math.radians(self.angle)
        self.scale = scale

    def reset(self):
        self.sprite.body.position = pymunk.Vec2d(self.x * self.scale, self.y * self.scale)
        self.sprite.body.angle = math.radians(self.angle)
        self.sprite.body.velocity = (0, 0)
        self.sprite.body.angular_velocity = 0

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        width = config['width']
        height = config['height']
        color = eval(config['color'])
        angle = config['angle']

        return cls(x, y, width, height, color, angle)
