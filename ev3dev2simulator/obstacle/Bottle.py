import arcade

from ev3dev2simulator.visualisation.PymunkRoundSprite import PymunkRoundSprite


class Bottle:
    """
    This class represents a 'bottle'. Bottles are circles.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 radius: float,
                 color: arcade.Color):

        self.x = x
        self.y = y
        self.radius = radius

        # visualisation
        self.color = color
        self.sprite = None

    @classmethod
    def from_config(cls, config):
        x = config['x']
        y = config['y']
        radius = config['radius']
        color = eval(config['color'])

        return cls(x, y, radius, color)

    def get_sprite(self):
        return self.sprite

    def create_sprite(self, scale):
        self.sprite = PymunkRoundSprite('assets/images/bottle.png',
                                        self.x * scale, self.y * scale, scale * 2 * (self.radius / 948))


