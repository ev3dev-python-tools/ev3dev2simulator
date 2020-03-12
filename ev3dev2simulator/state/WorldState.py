import os

from arcade import color

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

from ev3dev2simulator.obstacle.Ground import Ground
from ev3dev2simulator.obstacle.Border import Border
from ev3dev2simulator.obstacle.Bottle import Bottle
from ev3dev2simulator.obstacle.Edge import Edge
from ev3dev2simulator.obstacle.Lake import Lake
from ev3dev2simulator.obstacle.Rock import Rock
from ev3dev2simulator.robot.RobotLarge import RobotLarge
from ev3dev2simulator.robot.RobotSmall import RobotSmall
from ev3dev2simulator.util.Util import apply_scaling

from ev3dev2simulator.config.config import get_config


class WorldState:
    def __init__(self, config):
        self.obstacles = []
        self.touch_obstacles = []
        self.falling_obstacles = []
        self.color_obstacles = []
        self.robots = []

        # for key, value in config['robots'].items():
        #     print(key)
        # if self.large_sim_type:
        #     self.robot = RobotLarge(self.cfg, self.robot_pos[0], self.robot_pos[1], self.robot_pos[2])
        # else:
        #     self.robot = RobotSmall(self.cfg, self.robot_pos[0], self.robot_pos[1], self.robot_pos[2])
        #
        # for s in self.robot.get_sprites():
        #     self.robot_elements.append(s)
        #
        # for s in self.robot.get_sensors():
        #     self.robot_state.load_sensor(s)

        vis_config = get_config().get_visualisation_config()

        edge = Edge(vis_config)
        self.falling_obstacles.append(edge)

        for key, value in config['obstacles'].items():
            if value['type'] == 'lake':
                lake = Lake.from_config(value)
                self.obstacles.append(lake)
                self.falling_obstacles.append(lake.hole)
                self.color_obstacles.append(lake)
            elif value['type'] == 'rock':
                rock = Rock.from_config(value)
                self.obstacles.append(rock)
                self.touch_obstacles.append(rock)
            elif value['type'] == 'border':
                border = Border.from_config(vis_config, value)
                self.obstacles.append(border)
                self.color_obstacles.append(border)
            elif value['type'] == 'bottle':
                bottle = Bottle.from_config(value)
                self.obstacles.append(bottle)
                self.touch_obstacles.append(bottle)
            else:
                print("unknown obstacle type")

        # This should only be added if it has a measurement probe
        # ground = Ground(1460, 950, 300, 10, color.BLACK)
        # self.obstacles.append(ground)

