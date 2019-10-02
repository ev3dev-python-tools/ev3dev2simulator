"""
Main simulator class.
This class extends from arcade.Window and manages the updates and rendering of the simulator window.
"""

import arcade
from pymunk import Space

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

        super(Simulator, self).__init__(self.screen_width, self.screen_height, screen_title, update_rate=1 / 30)

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

        self.space = None

        self.center_cs_data = 0
        self.left_ts_data = False
        self.right_ts_data = False
        self.top_us_data = -1


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

        for s in self.robot.get_sensors():
            self.robot_state.load_sensor(s)

        self.blue_lake = BlueLake(self.cfg)
        self.green_lake = GreenLake(self.cfg)
        self.red_lake = RedLake(self.cfg)

        self.rock1 = Rock(550, 700, 100, 40, arcade.color.DARK_GRAY, 10)
        self.rock2 = Rock(650, 250, 200, 60, arcade.color.DARK_GRAY, 130)

        self.obstacle_elements.append(self.blue_lake.shape)
        self.obstacle_elements.append(self.green_lake.shape)
        self.obstacle_elements.append(self.red_lake.shape)

        self.obstacle_elements.append(self.rock1.shape)
        self.obstacle_elements.append(self.rock2.shape)

        self.border = Border(self.cfg, arcade.color.WHITE)

        for s in self.border.shapes:
            self.obstacle_elements.append(s)

        color_obstacles = [self.blue_lake, self.green_lake, self.red_lake, self.border]
        touch_obstacles = [self.rock1, self.rock2]

        self.robot.set_color_obstacles(color_obstacles)
        self.robot.set_touch_obstacles(touch_obstacles)

        self.space = Space()
        self.space.add(self.rock1.poly)
        self.space.add(self.rock2.poly)


    def on_draw(self):
        """
        Render the simulation. This is done in 30 frames per second.
        """

        arcade.start_render()

        self.robot_elements.draw()
        self.obstacle_elements.draw()

        self._draw_text()


    def _draw_text(self):
        center_cs = f"CS center:  {self.center_cs_data}"
        left_ts = f"TS right:      {self.right_ts_data}"
        right_ts = f"TS left:         {self.left_ts_data}"
        top_us = f"US top:        {int(round(self.top_us_data))}"

        message = self.robot_state.next_sound_job()
        sound = message if message else '-'

        arcade.draw_text(center_cs, self.screen_width - 125, self.screen_height - 45, arcade.color.WHITE, 10)
        arcade.draw_text(left_ts, self.screen_width - 125, self.screen_height - 60, arcade.color.WHITE, 10)
        arcade.draw_text(right_ts, self.screen_width - 125, self.screen_height - 75, arcade.color.WHITE, 10)
        arcade.draw_text(top_us, self.screen_width - 125, self.screen_height - 90, arcade.color.WHITE, 10)
        arcade.draw_text('Sound:', self.screen_width - 125, self.screen_height - 105, arcade.color.WHITE, 10)
        arcade.draw_text(sound, self.screen_width - 125, self.screen_height - 120, arcade.color.WHITE, 10,
                         anchor_y='top')


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
            address_us = self.robot.ultrasonic_sensor.address

            self.center_cs_data = self.robot.center_color_sensor.get_sensed_color()
            self.left_ts_data = self.robot.left_touch_sensor.is_touching()
            self.right_ts_data = self.robot.right_touch_sensor.is_touching()
            self.top_us_data = self.robot.ultrasonic_sensor.distance(self.space)

            self.robot_state.values[address_center_cs] = self.center_cs_data
            self.robot_state.values[address_left_ts] = self.left_ts_data
            self.robot_state.values[address_right_ts] = self.right_ts_data
            self.robot_state.values[address_us] = self.top_us_data

        self.robot_state.release_locks()


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """

    cfg = load_config()

    robot_state = get_robot_state()

    server_thread = ServerSocket(robot_state)
    server_thread.setDaemon(True)
    server_thread.start()

    sim = Simulator(cfg, robot_state)
    sim.setup()
    arcade.run()


if __name__ == "__main__":
    main()
