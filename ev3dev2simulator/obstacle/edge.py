"""
Module containing the class Edge, a class that describes the outer edge of the playground.
"""

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.obstacle.border_obstacle import BorderObstacle


class Edge(BorderObstacle):
    """
    The outer line surrounding the border. Used to detect if the robot is
    falling of the field.
    """

    def __init__(self, width, height):
        vis_config = get_simulation_settings()
        depth = int(vis_config['screen_settings']['edge_spacing'])
        edge_spacing = 0
        super(Edge, self).__init__(width, height, 1, depth, edge_spacing)

    def create_shape(self, scale):
        """
        Creates the shape of the edge.
        """
        self._calc_points(scale)

    @staticmethod
    def get_shapes():
        """
        Since the edge does not have a shape, but is only used for checking if the robot is out of the field, returns []
        """
        return []
