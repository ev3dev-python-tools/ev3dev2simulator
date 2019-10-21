from ev3dev2.simulator.obstacle.BorderObstacle import BorderObstacle
from ev3dev2.simulator.util.Util import apply_scaling


class Edge(BorderObstacle):
    """
    The outer line surrounding the border. Used to detect if the robot is
    falling of the field.
    """


    def __init__(self, cfg):
        depth = apply_scaling(cfg['screen_settings']['edge_spacing'])
        edge_spacing = 0

        super(Edge, self).__init__(cfg, 1, depth, edge_spacing)
