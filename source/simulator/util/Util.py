import math

import yaml


def get_circle_points(center_x: float,
                      center_y: float,
                      radius: float,
                      num_segments: int = 32) -> [(int, int)]:
    """
     Determine all the coordinate points located on the outline of a circle of given position and radius.
     The number of points, which correlates to the smoothness of the outline,
     is specified by the number of segments.
     """

    points = []

    for segment in range(num_segments):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = 2.0 * radius * math.cos(theta) + center_x
        y = 2.0 * radius * math.sin(theta) + center_y

        points.append((x, y))

    points.append(points[0])
    return points


def pythagoras(delta_x: int, delta_y: int) -> float:
    """
    Calculate Pythagoras' theorem
    """

    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


def load_config():
    """
    Load config data from config.yaml
    """

    with open('../../config/config.yaml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
