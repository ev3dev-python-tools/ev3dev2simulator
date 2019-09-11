"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""

import arcade

from source.simulator.UserThread import UserThread
from source.simulator.job.JobHandler import JobHandler
from source.simulator.obstacle.Border import Border
from source.simulator.obstacle.Lake import Lake
from source.simulator.obstacle.Rock import Rock
from source.simulator.robot.Robot import Robot
from source.simulator.util.Color import GREEN, BLUE, RED
from source.simulator.util.Util import load_config


class Simulator(arcade.Window):

    def __init__(self, config):
        self.cfg = config
        self.job_handler = JobHandler()

        self.screen_width = self.cfg["screen_settings"]["screen_width"]
        self.screen_height = self.cfg["screen_settings"]["screen_height"]
        screen_title = self.cfg["screen_settings"]["screen_title"]

        super().__init__(self.screen_width, self.screen_height, screen_title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.robot_elements = None
        self.obstacle_elements = None

        self.robot = None

        self.green_lake = None
        self.blue_lake = None
        self.red_lake = None

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

        self.robot = Robot(self.cfg['image_paths'], 300, 300)

        for s in self.robot.get_sprites():
            self.robot_elements.append(s)

        self.green_lake = Lake(200, 250, 30, GREEN)
        self.blue_lake = Lake(800, 600, 30, BLUE)
        self.red_lake = Lake(500, 150, 30, RED)

        self.rock1 = Rock(150, 600, 100, 40, arcade.color.DARK_GRAY, 0)
        self.rock2 = Rock(700, 250, 200, 60, arcade.color.DARK_GRAY, 130)

        self.obstacle_elements.append(self.green_lake.create())
        self.obstacle_elements.append(self.blue_lake.create())
        self.obstacle_elements.append(self.red_lake.create())

        self.obstacle_elements.append(self.rock1.create())
        self.obstacle_elements.append(self.rock1.create_outline())
        self.obstacle_elements.append(self.rock2.create())
        self.obstacle_elements.append(self.rock2.create_outline())

        self.border = Border(self.screen_width, self.screen_height, 16, 30, arcade.color.WHITE)

        for b in self.border.create():
            self.obstacle_elements.append(b)

        pass

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

        move_job = self.job_handler.next_move_job()

        if move_job is not None:
            self.robot.execute_move_job(move_job)


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    config = load_config()

    user_thread = UserThread()
    user_thread.start()

    sim = Simulator(config)
    sim.setup()
    arcade.run()


if __name__ == "__main__":
    main()
