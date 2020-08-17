"""
The world simulator module contains the WoldSimulator class which simulates the world
"""
import math

from ev3dev2simulator.state.robot_simulator import RobotSimulator
from ev3dev2simulator.state.world_state import WorldState
from ev3dev2simulator.config.config import get_simulation_settings


class WorldSimulator:
    """
    The world simulator contains the robot simulators and also simulates all other objects.
    It handles the space, the physics of all objects in the world.
    """
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
        """
        Used to request a reset, which will be handled in the update function
        """
        self.should_reset = True
        for robot_sim in self.robot_simulators:
            robot_sim.should_reset = True

    def update(self):
        """
        Resets the model of the world.
        """
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
