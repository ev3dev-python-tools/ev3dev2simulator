"""
The arm_floor module contains the class ArmFloor. A class representing the ground of the sidebar arm.
"""

from arcade import create_rectangle


class ArmFloor:
    """
    The class ArmFloor represents ground in the sidebar below an arm as seen from the side.
    """
    def __init__(self, width, height, color):
        self.width = width
        self.height = height

        # visualisation
        self.color = color
        self.shape = None

    def get_shapes(self):
        """
        Return the shape of the Floor.
        """
        return [self.shape]

    def create_shape(self, x, y, width, height):
        """
        Create the small and long rectangle shown below the sidebar arm.
        """
        self.shape = create_rectangle(x, y, width, height, self.color)
