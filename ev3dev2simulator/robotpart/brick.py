"""
Module containing the class Brick, which represent an ev3dev2 brick, a small square computer.
"""

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.body_part import BodyPart
from ev3dev2simulator.util.dimensions import Dimensions


class Brick(BodyPart):
    """
    Class representing the body of the simulated robot.
    """

    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['body']
        super().__init__(config, robot, Dimensions(dims['width'], dims['height']), 'brick')

    def setup_visuals(self, scale):
        vis_conf = get_simulation_settings()
        self.init_sprite(vis_conf['image_paths']['body'], scale)
