import math

import arcade
import pymunk
from arcade import Sprite


class Rock:
    """
    This class represents a 'rock'. Rocks are rectangles.
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: float,
                 height: float,
                 color: arcade.Color,
                 angle: int,
                 movable: bool):

        self.new_pos_y = None
        self.new_pos_x = None
        self.x = int(x)
        self.y = int(y)
        self.width = float(width)
        self.height = float(height)
        self.angle = int(angle)

        # visualisation
        self.color = color
        self.sprite = None
        self.scale = None

        # physics
        self.body = None
        self.shape = None
        self.movable = movable

    def get_pos(self):
        if self.new_pos_x and self.new_pos_y:
            return self.new_pos_x, self.new_pos_y
        return self.x, self.y

    @property
    def cur_angle(self):
        if hasattr(self, 'new_angle'):
            return self.new_angle
        return self.angle

    def create_shape(self, scale):
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

    def set_new_pos(self, pos):
        self.new_pos_y = (1 / self.scale) * pos.y
        self.new_pos_x = (1 / self.scale) * pos.x

    def create_sprite(self, scale):
        pos_x, pos_y = self.get_pos()
        self.sprite = Sprite('assets/images/brick.png', scale=scale * (self.width / 892),
                             center_x=pos_x * scale, center_y=pos_y * scale)
        self.sprite.width = scale * self.width
        self.sprite.height = scale * self.height
        self.sprite.color = self.color

    def reset(self):
        self.body.position = pymunk.Vec2d(self.x * self.scale, self.y * self.scale)
        self.body.angle = math.radians(self.angle)
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        width = config['width']
        height = config['height']
        color = eval(config['color'])
        angle = config['angle']
        movable = True if 'movable' not in config else config['movable']

        return cls(x, y, width, height, color, angle, movable)
