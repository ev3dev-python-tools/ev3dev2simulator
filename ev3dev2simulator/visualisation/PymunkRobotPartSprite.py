import arcade
import pymunk

# Default friction used for sprites, unless otherwise specified
from pymunk import Circle

from ev3dev2simulator.visualisation.PymunkSprite import DEFAULT_FRICTION, DEFAULT_MASS


class PymunkRobotPartSprite(arcade.Sprite):
    """
    We need a Sprite and a Pymunk physics object. This class blends them
    together.
    """

    def __init__(self,
                 src_list,
                 start_sprite=0,
                 x_offset=0,
                 y_offset=0,
                 width_mm=0,
                 height_mm=0,
                 scale=1,
                 friction=DEFAULT_FRICTION,
                 body=None):
        super().__init__()
        for texture in src_list:
            texture = arcade.load_texture(texture)
            self.append_texture(texture)

        px_mm_scale = scale
        self.scale = px_mm_scale * (width_mm / texture.width)
        self.set_texture(start_sprite)
        width = width_mm * px_mm_scale
        height = height_mm * px_mm_scale

        vs = [(0, 0), (width, 0), (width, height), (0, height)]
        t = pymunk.Transform(tx=x_offset * px_mm_scale - width/2, ty=y_offset * px_mm_scale - height/2)
        self.shape = pymunk.Poly(body, vs, transform=t)
        self.shape.friction = friction
