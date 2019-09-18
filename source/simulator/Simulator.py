"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""

import arcade

from simulator.sensor.SensorHandler import get_sensor_handler
from source.simulator.UserThread import UserThread
from source.simulator.job.JobHandler import get_job_handler
from source.simulator.obstacle.Border import Border
from source.simulator.obstacle.Lake import GreenLake, BlueLake, RedLake
from source.simulator.obstacle.Rock import Rock
from source.simulator.robot.Robot import Robot
from source.simulator.util.Util import load_config


class Simulator(arcade.Window):

    def __init__(self, config, job_handler, sensor_handler):
        self.cfg = config
        self.job_handler = job_handler
        self.sensor_handler = sensor_handler

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

        self.robot = Robot(self.cfg['image_paths'], 300, 400)

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

        left_move_job = self.job_handler.next_left_move_job()
        right_move_job = self.job_handler.next_right_move_job()

        if not (left_move_job is None and right_move_job is None):
            self.robot.execute_move_job(left_move_job, right_move_job)

        c = self.robot.center_color_sensor.get_sensed_color()
        print(str(c))
        # self.sensor_handler.color_center = c


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    config = load_config()

    job_handler = get_job_handler()
    sensor_handler = get_sensor_handler()

    user_thread = UserThread(job_handler, sensor_handler)
    user_thread.setDaemon(True)
    user_thread.start()

    sim = Simulator(config, job_handler, sensor_handler)
    sim.setup()
    arcade.run()


if __name__ == "__main__":
    main()
