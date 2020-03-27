import math

import arcade

from ev3dev2simulator.obstacle.TouchObstacle import TouchObstacle
from ev3dev2simulator.visualisation.PymunkQuadrilateralSprite import PymunkQuadrilateralSprite


class Rock(TouchObstacle):
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
        super(Rock, self).__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

        # visualisation
        self.color = color
        self.sprite = None

    def get_shapes(self):
        return [self.shape]

    def create_sprite(self, scale):
        self.sprite = PymunkQuadrilateralSprite('assets/images/brick.png',
                                                self.x * scale, self.y * scale, scale * (self.width / 892))
        self.sprite.body.angle = math.radians(self.angle)

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        width = config['width']
        height = config['height']
        color = eval(config['color'])
        angle = config['angle']

        return cls(x, y, width, height, color, angle)
