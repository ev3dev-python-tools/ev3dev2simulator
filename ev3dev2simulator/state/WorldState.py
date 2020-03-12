import os



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


class WorldState:
    def __init__(self, config):
        self.obstacles = []
        self.touch_obstacles = []
        self.falling_obstacles = []
        self.color_obstacles = []
        self.robots = []

        # for key, value in config['robots'].items():
        #     print(key)

        for key, value in config['obstacles'].items():
            if value['type'] == 'lake':
                lake = Lake.from_config(value)
                self.obstacles.append(lake)
                self.falling_obstacles.append(lake)
                self.color_obstacles.append(lake)
            elif value['type'] == 'rock':
                self.obstacles.append(Rock.from_config(value))
            else:
                print("unknown obstacle type")
            print(key, value)

        ground = Ground()

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

        # self.border = Border(self.cfg, eval(self.cfg['obstacle_settings']['border_settings']['border_color']))
        # self.edge = Edge(self.cfg)
        #
        # for s in self.border.shapes:
        #     self.obstacle_elements.append(s)
        #
        # self.space = Space()
        #
        # if self.large_sim_type:
        #     self.rock1 = Rock(apply_scaling(825), apply_scaling(1050), apply_scaling(150), apply_scaling(60),
        #                       arcade.color.DARK_GRAY, 10)
        #     self.rock2 = Rock(apply_scaling(975), apply_scaling(375), apply_scaling(300), apply_scaling(90),
        #                       arcade.color.DARK_GRAY, 130)
        #
        #     self.ground = arcade.create_rectangle(apply_scaling(1460), apply_scaling(950), apply_scaling(300),
        #                                           apply_scaling(10),
        #                                           arcade.color.BLACK)
        #
        #     self.obstacle_elements.append(self.rock1.shape)
        #     self.obstacle_elements.append(self.rock2.shape)
        #     self.obstacle_elements.append(self.ground)
        #
        #     touch_obstacles = [self.rock1, self.rock2]
        #     falling_obstacles = [self.blue_lake.hole, self.green_lake.hole, self.red_lake.hole, self.edge]
        #
        #     self.space.add(self.rock1.poly)
        #     self.space.add(self.rock2.poly)
        #
        # else:
        #     self.bottle1 = Bottle(apply_scaling(1000), apply_scaling(300), apply_scaling(40),
        #                           arcade.color.DARK_OLIVE_GREEN)
        #     self.obstacle_elements.append(self.bottle1.shape)
        #
        #     touch_obstacles = [self.bottle1]
        #     falling_obstacles = [self.edge]
        #
        #     self.space.add(self.bottle1.poly)
        #
        # color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]
        #
        # self.robot.set_color_obstacles(color_obstacles)
        # self.robot.set_touch_obstacles(touch_obstacles)
        # self.robot.set_falling_obstacles(falling_obstacles)
