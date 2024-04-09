"""
Module containing the point class
"""
from dataclasses import dataclass


@dataclass
class Point:
    """Class for keeping a single 2D coordinate"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
