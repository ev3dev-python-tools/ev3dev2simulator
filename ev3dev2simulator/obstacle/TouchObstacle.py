import arcade
from arcade import SpriteList


class TouchObstacle:
    """
    This class provides basic functionality for obstacles which can be interacted with using touch.
    """

    def __init__(self):
        self.points = None
        self.poly = None

    def collided_with(self, sprite: arcade.Sprite) -> bool:
        """
        Check if this obstacle has collided with the given sprite.
        :param sprite: to check collision for.
        :return: True if collision detected.
        """
        return arcade.check_for_collision_with_list(self.sprite, SpriteList().append(sprite))
