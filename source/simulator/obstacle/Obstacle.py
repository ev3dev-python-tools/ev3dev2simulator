import arcade


class Obstacle:
    """
    This class provides basic functionality for obstacles. These include color coding
    and collision detection.
    """


    def __init__(self, color_code: int):
        self.color_code = color_code
        self.points = None


    def collided_with(self, sprite: arcade.Sprite) -> bool:
        """
        Check if this obstacle has collided with the given sprite.
        :param sprite: to check collision for.
        :return: True if collision detected.
        """

        return arcade.are_polygons_intersecting(self.points, sprite.points)
