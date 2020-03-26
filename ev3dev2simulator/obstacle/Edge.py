from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.obstacle.BorderObstacle import BorderObstacle


class Edge(BorderObstacle):
    """
    The outer line surrounding the border. Used to detect if the robot is
    falling of the field.
    """

    def __init__(self, width, height):
        vis_config = get_simulation_settings()
        depth = vis_config['screen_settings']['edge_spacing']
        edge_spacing = 0
        super(Edge, self).__init__(width, height, 1, depth, edge_spacing)

    def create_shape(self, scale):
        self._calc_points(scale)

    def get_shapes(self):
        return []
