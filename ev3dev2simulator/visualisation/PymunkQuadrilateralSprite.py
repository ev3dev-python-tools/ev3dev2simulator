import pymunk

# Default friction used for sprites, unless otherwise specified
from ev3dev2simulator.visualisation.PymunkSprite import PymunkSprite, DEFAULT_FRICTION, DEFAULT_MASS


class PymunkQuadrilateralSprite(PymunkSprite):
    """
    We need a Sprite and a Pymunk physics object. This class blends them
    together.
    """

    def __init__(self,
                 filename,
                 center_x=0,
                 center_y=0,
                 scale=1,
                 mass=DEFAULT_MASS,
                 moment=None,
                 friction=DEFAULT_FRICTION,
                 body_type=pymunk.Body.DYNAMIC):
        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)

        width = self.texture.width * scale
        height = self.texture.height * scale

        if moment is None:
            moment = pymunk.moment_for_box(mass, (width, height))

        self.body = pymunk.Body(mass, moment, body_type=body_type)
        self.body.position = pymunk.Vec2d(center_x, center_y)

        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.friction = friction
