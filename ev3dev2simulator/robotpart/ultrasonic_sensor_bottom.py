"""
The ultrasonic_sensor_top module contains the class UltrasonicSensorBottom class.
It represents an ultrasonic sensor that aims to the ground.
"""


from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.robotpart.body_part import BodyPart
from ev3dev2simulator.util.dimensions import Dimensions
from ev3dev2simulator.obstacle.hole import Hole
from ev3dev2simulator.obstacle.board import Board


class UltrasonicSensorBottom(BodyPart):
    """
    Class representing an UltrasonicSensor of the simulated robot mounted towards the ground.
    """
    def __init__(self, config, robot):
        dims = get_simulation_settings()['body_part_sizes']['ultrasonic_sensor_bottom']
        super(UltrasonicSensorBottom, self).__init__(config, robot, Dimensions(dims['width'], dims['height']),
                                                     'ultrasonic_sensor', driver_name='lego-ev3-us')

    def setup_visuals(self, scale):
        img_cfg = get_simulation_settings()['image_paths']
        self.init_sprite(img_cfg['ultrasonic_sensor_bottom'], scale)

    def get_latest_value(self):
        """
        Gets the current distance to the ground (a fixed value) or
        the max distance measured if there is a hole in the ground.
        """
        return self.distance()

    def distance(self) -> float:
        """
        Get the distance in pixels between this ultrasonic sensor and an the ground.
        :return: a floating point value representing the distance.
        """
        for obstacle in self.sensible_obstacles:
            if obstacle.collided_with(self.sprite.center_x, self.sprite.center_y):
                if isinstance(obstacle, Hole):
                    return obstacle.depth
                if isinstance(obstacle, Board):
                    return 20
                return self.get_default_value()
        return self.get_default_value()

    def get_default_value(self):
        """
        1 pixel == 1mm so measurement values this sensor returns are one to one mappable to millimeters.
        Max distance real world robotpart ultrasonic sensor returns is 2550mm.
        :return: default value in pixels.
        """
        return 2550
