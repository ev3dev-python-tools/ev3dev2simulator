"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""

import arcade

from simulator.connection.ServerSocket import ServerSocket
from simulator.obstacle.Border import Border
from simulator.obstacle.Lake import GreenLake, BlueLake, RedLake
from simulator.obstacle.Rock import Rock
from simulator.robot.Robot import Robot
from simulator.state.RobotState import get_robot_state
from simulator.util.Util import load_config


class Simulator(arcade.Window):

    def __init__(self, config, robot_state):
        self.cfg = config
        self.robot_state = robot_state

        self.screen_width = self.cfg['screen_settings']['screen_width']
        self.screen_height = self.cfg['screen_settings']['screen_height']
        screen_title = self.cfg['screen_settings']['screen_title']

        super().__init__(self.screen_width, self.screen_height, screen_title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.robot_elements = None
        self.obstacle_elements = None

        self.robot = None

        self.red_lake = None
        self.green_lake = None
        self.blue_lake = None

        self.rock1 = None
        self.rock2 = None

        self.border = None


    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.obstacle_elements = arcade.ShapeElementList()

        self.robot = Robot(self.cfg, 300, 400)

        for s in self.robot.get_sprites():
            self.robot_elements.append(s)

        self.blue_lake = BlueLake(self.cfg)
        self.green_lake = GreenLake(self.cfg)
        self.red_lake = RedLake(self.cfg)

        self.rock1 = Rock(550, 700, 100, 40, arcade.color.DARK_GRAY, 10)
        self.rock2 = Rock(650, 250, 200, 60, arcade.color.DARK_GRAY, 130)

        self.obstacle_elements.append(self.blue_lake.create())
        self.obstacle_elements.append(self.green_lake.create())
        self.obstacle_elements.append(self.red_lake.create())

        self.obstacle_elements.append(self.rock1.create())
        self.obstacle_elements.append(self.rock2.create())

        self.border = Border(self.cfg, arcade.color.WHITE)

        for b in self.border.create():
            self.obstacle_elements.append(b)

        color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]
        touch_obstacles = [self.rock1, self.rock2]

        self.robot.set_color_obstacles(color_obstacles)
        self.robot.set_touch_obstacles(touch_obstacles)


    def on_draw(self):
        """
        Render the simulation. This is done in 60 frames per second.
        """

        arcade.start_render()

        self.robot_elements.draw()
        self.obstacle_elements.draw()


    def update(self, delta_time):
        """
        All the logic to move the robot. Collision detection is also performed.
        """

        if self.robot_state.should_reset:
            self.setup()
            self.robot_state.reset()

        else:
            left_ppf = self.robot_state.next_left_move_job()
            right_ppf = self.robot_state.next_right_move_job()

            if left_ppf or right_ppf:
                self.robot.execute_movement(left_ppf, right_ppf)

            address_center_cs = self.robot.center_color_sensor.address
            address_left_ts = self.robot.left_touch_sensor.address
            address_right_ts = self.robot.right_touch_sensor.address

            self.robot_state.values[address_center_cs] = self.robot.center_color_sensor.get_sensed_color()
            self.robot_state.values[address_left_ts] = self.robot.left_touch_sensor.is_touching()
            self.robot_state.values[address_right_ts] = self.robot.right_touch_sensor.is_touching()


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    config = load_config()

    robot_state = get_robot_state()

    server_thread = ServerSocket(robot_state)
    server_thread.setDaemon(True)
    server_thread.start()

    sim = Simulator(config, robot_state)
    sim.setup()
    arcade.run()


if __name__ == "__main__":
    main()
