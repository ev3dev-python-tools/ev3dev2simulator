"""
Module movable_object contains the class MovableObject.
"""
import math

import arcade as _arcade
import pymunk

from ev3dev2simulator.util.point import Point


class MovableObject:
    """
    Super class for all object that should move when the robot pushed against it.
    """
    def __init__(self,
                 pos: Point,
                 angle: int,
                 color: _arcade.Color):

        self.x = pos.x
        self.y = pos.y
        self.angle = angle

        # visualisation
        self.color = color
        self.sprite = None
        self.scale = None

        # physics
        self.body = None
        self.shape = None
        self.new_pos_x = None
        self.new_pos_y = None

    def get_pos(self):
        """
        Returns the current position of the rock.
        """
        if self.new_pos_x and self.new_pos_y:
            return self.new_pos_x, self.new_pos_y
        return self.x, self.y

    def set_new_pos(self, pos):
        """
        Sets the current position of the bottle.
        """
        self.new_pos_x = (1 / self.scale) * pos.x
        self.new_pos_y = (1 / self.scale) * pos.y

    def reset(self):
        """
        Resets the position and the speed of the rock.
        """
        self.body.position = pymunk.Vec2d(self.x * self.scale, self.y * self.scale)
        self.body.angle = math.radians(self.angle)
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
