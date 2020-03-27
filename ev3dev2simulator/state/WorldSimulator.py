import math

from ev3dev2simulator.state.RobotSimulator import RobotSimulator
from ev3dev2simulator.state.WorldState import WorldState


class WorldSimulator:
    def __init__(self, world_state: WorldState):
        self.world_state = world_state
        self.robotSimulators = []
        for robot in world_state.robots:
            robot_sim = RobotSimulator(robot)
            self.robotSimulators.append(robot_sim)

        self.world_state.space.add_default_collision_handler()

    def update(self):

        self.resync_physics_sprites()
        self.world_state.space.step(1.0 / 30.0)
        for robot in self.robotSimulators:
            robot.update()

    def resync_physics_sprites(self):
        """ Move sprites to where physics objects are """
        for sprite in self.world_state.sprite_list:
            sprite.center_x = sprite.shape.body.position.x
            sprite.center_y = sprite.shape.body.position.y
            sprite.angle = math.degrees(sprite.shape.body.angle)
