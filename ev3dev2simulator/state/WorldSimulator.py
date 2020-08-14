import math

from ev3dev2simulator.state.RobotSimulator import RobotSimulator
from ev3dev2simulator.state.WorldState import WorldState
from ev3dev2simulator.config.config import get_simulation_settings


class WorldSimulator:
    def __init__(self, world_state: WorldState):
        self.world_state = world_state
        self.robot_simulators = []
        self.should_reset = False
        for robot in world_state.robots:
            robot_sim = RobotSimulator(robot)
            self.robot_simulators.append(robot_sim)

        self.world_state.space.add_default_collision_handler()

        self.space_step_size = float(get_simulation_settings()['exec_settings']['frames_per_second'])

    def request_reset(self):
        self.should_reset = True
        for robot_sim in self.robot_simulators:
            robot_sim.should_reset = True

    def update(self):
        if self.should_reset:
            self.world_state.reset()
            self.should_reset = False
        else:
            self.sync_physics_sprites()
            self.world_state.space.step(1.0 / self.space_step_size)
            for robot in self.robot_simulators:
                robot.update()

    def sync_physics_sprites(self):
        """ Move sprites to where physics objects are """
        for obstacle in self.world_state.obstacles:
            obstacle.sprite.center_x = obstacle.body.position.x
            obstacle.sprite.center_y = obstacle.body.position.y
            obstacle.sprite.angle = math.degrees(obstacle.body.angle)
            obstacle.set_new_pos(obstacle.body.position)
            obstacle.new_angle = obstacle.sprite.angle
