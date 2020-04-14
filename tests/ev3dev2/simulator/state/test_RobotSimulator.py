import unittest
from unittest.mock import MagicMock

from ev3dev2simulator.state.RobotSimulator import RobotSimulator
from ev3dev2simulator.state.RobotState import RobotState
from tests.ev3dev2.simulator.state.test_RobotState import TestRobotState


class TestRobotSimulator(unittest.TestCase):
    def test_constructor(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        state.setup_pymunk_shapes(1)
        sim = RobotSimulator(state)
        sim._sync_physics_sprites = MagicMock()
        sim.update()
        self.assertEqual(True, True)
        sim.reset()
        sim.release_locks()


    def test_get_value(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        state.setup_pymunk_shapes(1)
        sim = RobotSimulator(state)
        sim._sync_physics_sprites = MagicMock()
        val = sim.get_value((0, 'ev3-ports:in4'))
        self.assertEqual(val, 2550)


if __name__ == '__main__':
    unittest.main()
