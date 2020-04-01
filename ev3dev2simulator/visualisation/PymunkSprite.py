import arcade

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

# Default mass used for sprites
DEFAULT_MASS = 5


class PymunkSprite(arcade.Sprite):
    """
    We need a Sprite and a Pymunk physics object. This class blends them
    together.
    """

    def __init__(self,
                 filename,
                 center_x=0,
                 center_y=0,
                 scale=1):
        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)
        self.body = None
        self.shape = None
