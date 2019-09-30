import math
from typing import Tuple

import yaml


def get_circle_points(center_x: float,
                      center_y: float,
                      radius: float,
                      num_segments: int = 32) -> [(int, int)]:
    """
    Determine all the coordinate points located on the outline of a circle of given position and radius.
    The number of points, which correlates to the smoothness of the outline,
    is specified by the number of segments.

    :param center_x: the x coordinate of the created circle center.
    :param center_y: the y coordinate of the created circle center.
    :param radius: the radius of the created circle.
    :param num_segments: the number of segments of the circle outline.
    :return: a list of tuples containing the coordinates of the circle points.
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


def pythagoras(x: int, y: int) -> float:
    """
    Calculate Pythagoras' theorem
    :param x: length of one side.
    :param y: length of the other one side.
    :return: a floating point value representing the length of the third side.
    """

    return math.sqrt(x * x + y * y)


def load_config():
    """
    Load config data from config.yaml
    :return: the config data.
    """

    with open('../../config/config.yaml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def calc_differential_steering_angle_x_y(b: int, dl: float, dr: float, o: float) -> Tuple[float, float, float]:
    """
    Calculate the next orientation, x and y values of a two-wheel
    propelled object based on the differential steering principle.

    :param b: the distance between the two wheels.
    :param dl: linear displacement of the left motor in pixels.
    :param dr: linear displacement of the right motor in pixels.
    :param o: current orientation of the object in radians.
    :return: the new orientation in degrees and the new x and y values in pixels.
    """

    dc = (dr + dl) / 2
    diff_angle = (dr - dl) / b

    diff_x = dc * math.cos(diff_angle + o)
    diff_y = dc * math.sin(diff_angle + o)

    return diff_angle, diff_x, diff_y
