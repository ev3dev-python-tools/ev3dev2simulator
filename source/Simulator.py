"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""

import arcade

from source.UserThread import UserThread
from source.job.JobHandler import JobHandler
from source.obstacle.Lake import Lake
from source.obstacle.Rock import Rock
from source.robot.Robot import Robot
from source.util.Color import GREEN, BLUE, RED
from source.util.Util import load_config


class Simulator(arcade.Window):

    def __init__(self, config, job_handler):
        self.cfg = config
        self.job_handler = job_handler

        screen_width = self.cfg["screen_settings"]["screen_width"]
        screen_height = self.cfg["screen_settings"]["screen_height"]
        screen_title = self.cfg["screen_settings"]["screen_title"]

        super().__init__(screen_width, screen_height, screen_title)

        arcade.set_background_color(arcade.color.GOLDEN_BROWN)

        self.robot_elements = None
        self.lake_elements = None
        self.rock_elements = None

        self.robot = None

        self.green_lake = None
        self.blue_lake = None
        self.red_lake = None

        self.rock1 = None
        self.rock2 = None

    def setup(self):
        """
        Set up all the necessary shapes and sprites which are used in the simulation.
        These elements are added to lists to make buffered rendering possible to improve performance.
        """

        self.robot_elements = arcade.SpriteList()
        self.lake_elements = arcade.ShapeElementList()
        self.rock_elements = arcade.ShapeElementList()

        self.robot = Robot(self.cfg['image_paths'], 300, 300)

        for s in self.robot.get_sprites():
            self.robot_elements.append(s)

        self.green_lake = Lake(200, 200, 30, GREEN)
        self.blue_lake = Lake(300, 300, 30, BLUE)
        self.red_lake = Lake(400, 400, 30, RED)

        self.rock1 = Rock(100, 100, 100, 40, arcade.color.DARK_GRAY, 10)
        self.rock2 = Rock(600, 300, 200, 20, arcade.color.DARK_GRAY, 40)

        self.lake_elements.append(self.green_lake.create())
        self.lake_elements.append(self.blue_lake.create())
        self.lake_elements.append(self.red_lake.create())

        self.rock_elements.append(self.rock1.create())
        self.rock_elements.append(self.rock1.create_outline())
        self.rock_elements.append(self.rock2.create())
        self.rock_elements.append(self.rock2.create_outline())

        pass

    def on_draw(self):
        """
        Render the simulation. This is done in 60 frames per second.
        """

        arcade.start_render()

        self.robot_elements.draw()
        self.lake_elements.draw()
        self.rock_elements.draw()

    def update(self, delta_time):
        """
        All the logic to move the robot. Collison detection is also performed.
        """

        move_job = self.job_handler.get_next_move_job()
        rotate_job = self.job_handler.get_next_rotate_job()

        self.robot.move_x(move_job.delta_x)
        self.robot.move_y(move_job.delta_y)

        self.robot.rotate(rotate_job.degrees)


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    config = load_config()
    job_handler = JobHandler()

    user_thread = UserThread(job_handler)
    user_thread.start()

    sim = Simulator(config, job_handler)
    sim.setup()
    arcade.run()


if __name__ == "__main__":
    main()
