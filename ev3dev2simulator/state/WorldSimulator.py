from ev3dev2simulator.state.RobotSimulator import RobotSimulator
from ev3dev2simulator.state.WorldState import WorldState


class WorldSimulator:
    def __init__(self, world_state: WorldState):
        self.world_state = world_state
        self.robotSimulators = []
        for robot in world_state.robots:
            robot_sim = RobotSimulator(robot)
            self.robotSimulators.append(robot_sim)

    def update(self):
        self.world_state.space.step(1 / 30.0)
        for robot in self.robotSimulators:
            robot.update()
