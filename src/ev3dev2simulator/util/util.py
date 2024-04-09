"""
Module containing various utility function, mostly concerning mathematical 2D calculations.
"""

import math
from typing import Tuple

import arcade as _arcade
from arcade import PointList


def get_circle_points(center_x: float,
                      center_y: float,
                      radius: float,
                      num_segments: int = 32) -> PointList:
    """
    Determine all the coordinate points located on the outline of a circle of given position and radius.
    The number of points, which correlates to the smoothness of the outline,
    is specified by the number of segments.

    :param center_x: the x coordinate of the created circle center.
    :param center_y: the y coordinate of the created circle center.
    :param radius: the radius of the created circle.
    :param num_segments: the number of segments of the circle outline.
    :return: a PointList object containing the coordinates of the circle points.
    """

    points = []

    for segment in range(num_segments):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = radius * math.cos(theta) + center_x
        y = radius * math.sin(theta) + center_y

        points.append((x, y))

    points.append(points[0])
    points.append(points[1])
    return points


def distance_between_points(x_of_point1: float, y_of_point1: float, x_of_point2: float, y_of_point2: float) -> float:
    """
    Calculate the distance between two points in 2D space.
    :param x_of_point1: coordinate of point 1
    :param y_of_point1: coordinate of point 1
    :param x_of_point2: coordinate of point 2
    :param y_of_point2: coordinate of point 2
    :return: a floating point value representing the distance.
    """

    return math.hypot(x_of_point2 - x_of_point1, y_of_point2 - y_of_point1)


def calc_differential_steering_angle_x_y(wheel_space: int, left_displacement: float,
                                         right_displacement: float, orientation: float) -> Tuple[float, float, float]:
    """
    Calculate the next orientation, x and y values of a two-wheel
    propelled object based on the differential steering principle.

    :param wheel_space: the distance between the two wheels.
    :param left_displacement: linear displacement of the left motor in pixels.
    :param right_displacement: linear displacement of the right motor in pixels.
    :param orientation: current orientation of the object in radians.
    :return: the new orientation in degrees and the new x and y values in pixels.
    """

    center_displacement = (right_displacement + left_displacement) / 2
    diff_angle = (right_displacement - left_displacement) / wheel_space

    diff_x = center_displacement * math.cos(diff_angle + orientation)
    diff_y = center_displacement * math.sin(diff_angle + orientation)

    return diff_angle, diff_x, diff_y


def get_cm_multiplier() -> float:
    """
    Get the multiplier needed for converting millimeters to centimeters.
    :return: a floating point value representing the multiplier.
    """

    return 0.1


def get_inch_multiplier() -> float:
    """
    Get the multiplier needed for converting millimeters to inches.
    :return: a floating point value representing the multiplier.
    """

    return 0.254


def to_color_code(color: _arcade.Color) -> int:
    """
    Convert rgb tuple to ev3dev color
    """
    switcher = {
        (59, 60, 54): 1,  # Black
        (58, 166, 221): 2,  # Blue
        (122, 182, 72): 3,  # Green
        (252, 227, 3): 4,  # Yellow
        (201, 45, 57): 5,  # Red
        (235, 235, 235): 6,  # White
        (255, 255, 255): 6  # White
    }

    return switcher.get(color, 0)
