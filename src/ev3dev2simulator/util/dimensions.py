"""
Module containing the point class
"""
from dataclasses import dataclass


@dataclass
class Dimensions:
    """Class for keeping dimensions of an object using width and height"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __iter__(self):
       newtuple=(self.width,self.height)
       return newtuple.__iter__() 
