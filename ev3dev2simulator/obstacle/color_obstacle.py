"""
module color_obstacle containing the abstract class ColorObstacle.
"""


class ColorObstacle:
    """
    This class provides basic functionality for obstacles which can be interacted with using color sensing.
    """

    def __init__(self, color_code: int):
        self.color_code = color_code

    def collided_with(self, x: float, y: float) -> bool:
        """
        Check if this obstacle has collided with the given Point. Meaning the point is inside this obstacle.
        :param x: coordinate of the point.
        :param y: coordinate of the point.
        :return: True if collision detected.
        """

    def get_color_code(self):
        """
        Returns the saved color code
        """
        return self.color_code
