import arcade
import pymunk
from pymunk import Space

from ev3dev2simulator.obstacle.Board import Board
from ev3dev2simulator.state.RobotState import RobotState

from ev3dev2simulator.obstacle.Border import Border
from ev3dev2simulator.obstacle.Bottle import Bottle
from ev3dev2simulator.obstacle.Edge import Edge
from ev3dev2simulator.obstacle.Lake import Lake
from ev3dev2simulator.obstacle.Rock import Rock
from ev3dev2simulator.visualisation.PymunkSprite import PymunkSprite


class WorldState:
    def __init__(self, config):
        self.sprite_list = arcade.SpriteList[PymunkSprite]()
        self.obstacles = []
        self.static_obstacles = []
        self.touch_obstacles = []
        self.falling_obstacles = []
        self.color_obstacles = []

        self.robots = []
        self.space = Space()
        self.space.damping = 0.99

        self.board_width = int(config['board_width'])
        self.board_height = int(config['board_height'])
        board_color = eval(config['board_color'])

        board = Board(self.board_width / 2, self.board_height / 2, self.board_width, self.board_height, board_color)
        self.static_obstacles.append(board)

        for robot_conf in config['robots']:
            self.robots.append(RobotState(robot_conf))

        edge = Edge(self.board_width, self.board_height)
        self.static_obstacles.append(edge)
        self.falling_obstacles.append(edge)

        for key, value in config['obstacles'].items():
            if value['type'] == 'lake':
                lake = Lake.from_config(value)
                self.static_obstacles.append(lake)
                if lake.hole is not None:
                    self.falling_obstacles.append(lake.hole)
                self.color_obstacles.append(lake)
            elif value['type'] == 'rock':
                rock = Rock.from_config(value)
                self.obstacles.append(rock)
                self.touch_obstacles.append(rock)
            elif value['type'] == 'border':
                border = Border.from_config(self.board_width, self.board_height, value)
                self.static_obstacles.append(border)
                self.color_obstacles.append(border)
            elif value['type'] == 'bottle':
                bottle = Bottle.from_config(value)
                self.obstacles.append(bottle)
                self.touch_obstacles.append(bottle)
            else:
                print("unknown obstacle type")

        self.color_obstacles.append(board)

    def setup_visuals(self, scale):

        for obstacle in self.static_obstacles:
            obstacle.create_shape(scale)

        touch_sprites = arcade.SpriteList[PymunkSprite]()

        for obstacle in self.obstacles:
            obstacle.create_sprite(scale)
            self.sprite_list.append(obstacle.sprite)
            touch_sprites.append(obstacle.sprite)

        for sprite in self.sprite_list:
            self.space.add(sprite.body)
            self.space.add(sprite.shape)

        for idx, robot in enumerate(self.robots):
            robot.setup_visuals(scale)
            for sprite in robot.get_sprites():
                sprite.shape.filter = pymunk.ShapeFilter(group=idx+5)
                self.space.add(sprite.shape)
            self.space.add(robot.body)
            robot.set_color_obstacles(self.color_obstacles)
            robot.set_touch_obstacles(touch_sprites)
            robot.set_falling_obstacles(self.falling_obstacles)

    def get_robots(self) -> [RobotState]:
        return self.robots
