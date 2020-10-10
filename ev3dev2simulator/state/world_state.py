"""
The world state module contains the state of the world, which includes the robot states.
"""

from math import radians

import arcade as _arcade
import pymunk
from pymunk import Space

from ev3dev2simulator.obstacle.board import Board
from ev3dev2simulator.state.robot_state import RobotState

from ev3dev2simulator.obstacle.border import Border
from ev3dev2simulator.obstacle.bottle import Bottle
from ev3dev2simulator.obstacle.edge import Edge
from ev3dev2simulator.obstacle.lake import Lake
from ev3dev2simulator.obstacle.rock import Rock


class WorldState:
    """
    Contains the objects, the robots and the surrounding space of the 'world'
    """
    def __init__(self, config):
        self.sprite_list = _arcade.SpriteList()
        self.obstacles = []
        self.static_obstacles = []
        self.falling_obstacles = []
        self.color_obstacles = []

        self.robots = []
        self.space = Space()
        self.space.damping = 0.1

        self.board_width = config['board_width']
        self.board_height = config['board_height']
        board_color = tuple(config['board_color'])

        board = Board(self.board_width / 2, self.board_height / 2, self.board_width, self.board_height, board_color)
        self.static_obstacles.append(board)

        for robot_conf in config['robots']:
            self.robots.append(RobotState(robot_conf))

        edge = Edge(self.board_width, self.board_height)
        self.static_obstacles.append(edge)
        self.falling_obstacles.append(edge)

        for obstacle in config['obstacles']:
            if obstacle['type'] == 'lake':
                lake = Lake.from_config(obstacle)
                self.static_obstacles.append(lake)
                if lake.hole is not None:
                    self.falling_obstacles.append(lake.hole)
                self.color_obstacles.append(lake)
            elif obstacle['type'] == 'rock':
                rock = Rock.from_config(obstacle)
                self.obstacles.append(rock)
            elif obstacle['type'] == 'border':
                border = Border.from_config(self.board_width, self.board_height, obstacle)
                self.static_obstacles.append(border)
                self.color_obstacles.append(border)
            elif obstacle['type'] == 'bottle':
                bottle = Bottle.from_config(obstacle)
                self.obstacles.append(bottle)
            else:
                print("unknown obstacle type")

        self.color_obstacles.append(board)

        self.selected_object = None

    def reset(self):
        """
        Reset all obstacles in the world (except robots) to their original position.
        """
        for obstacle in self.obstacles:
            obstacle.reset()

    def setup_pymunk_shapes(self, scale):
        """
        Setup the shapes that are added to the pymunk space.
        The robot get a shape filter so it does not interact with itself.
        """
        for idx, robot in enumerate(self.robots):
            robot_shapes = robot.setup_pymunk_shapes(scale)
            for shape in robot_shapes:
                shape.filter = pymunk.ShapeFilter(group=idx+5)
                self.space.add(shape)
            self.space.add(robot.body)

        for obstacle in self.obstacles:
            obstacle.create_shape(scale)
            self.space.add(obstacle.body)
            self.space.add(obstacle.shape)

    def rescale(self, new_scale):
        """
        On screen rescale, rescale all sprites.
        """
        for robot in self.robots:
            robot.shapes = []
        for obstacle in self.obstacles:
            obstacle.shape = None
        self.space.remove(self.space.shapes)
        self.space.remove(self.space.bodies)

        for robot in self.robots:
            robot.sprite_list = _arcade.SpriteList()
        self.sprite_list = _arcade.SpriteList()
        self.setup_pymunk_shapes(new_scale)
        self.setup_visuals(new_scale)

    def setup_visuals(self, scale):
        """
        Setup all sprites.
        """
        for obstacle in self.static_obstacles:
            obstacle.create_shape(scale)

        for obstacle in self.obstacles:
            obstacle.create_sprite(scale)
            self.sprite_list.append(obstacle.sprite)

        for robot in self.robots:
            robot.setup_visuals(scale)
            robot.set_color_obstacles(self.color_obstacles)
            robot.set_falling_obstacles(self.falling_obstacles)

    def set_object_at_position_as_selected(self, pos):
        """
        Based on the position given, select the object that is closest (with a maximum of 15) and set as selected.
        """
        max_distance = 15
        queried_object = self.space.point_query_nearest(pos, max_distance, pymunk.ShapeFilter())
        if queried_object is not None:
            poly = queried_object.shape
            if hasattr(poly, 'body'):
                self.selected_object = poly.body

    def move_selected_object(self, delta_x, delta_y):
        """
        Move the selected object with the given offset.
        """
        if self.selected_object:
            self.selected_object.position += (delta_x, delta_y)

    def rotate_selected_object(self, delta_angle):
        """
        Rotate the selected object with the given angle.
        """
        if self.selected_object is not None:
            self.selected_object.angle += radians(delta_angle)

    def unselect_object(self):
        """
        Deselect the previously selected object.
        """
        self.selected_object = None

    def get_robots(self) -> [RobotState]:
        """
        Gets the objects that are on the playing field.
        """
        return self.robots
