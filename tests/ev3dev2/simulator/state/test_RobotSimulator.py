import unittest
from unittest.mock import MagicMock

from ev3dev2simulator.state.RobotSimulator import RobotSimulator
from ev3dev2simulator.state.RobotState import RobotState
from tests.ev3dev2.simulator.state.test_RobotState import TestRobotState


class TestRobotSimulator(unittest.TestCase):
    def test_constructor_and_reset(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        state.setup_pymunk_shapes(1)
        sim = RobotSimulator(state)
        sim._sync_physics_sprites = MagicMock()
        sim.update()

        sim._sync_physics_sprites.assert_called_once()
        sim.should_reset = True
        self.assertEqual(sim.should_reset, True)
        sim.reset()
        self.assertEqual(sim.should_reset, False)
        sim.release_locks()

    def test_get_value_and_locks(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        state.setup_pymunk_shapes(1)
        sim = RobotSimulator(state)
        sim._sync_physics_sprites = MagicMock()
        val = sim.get_value((0, 'ev3-ports:in4'))
        self.assertEqual(val, 2550)
        self.assertEqual(sim.locks[(0, 'ev3-ports:in4')].locked(), True)
        sim.update()
        self.assertEqual(sim.locks[(0, 'ev3-ports:in4')].locked(), False)


if __name__ == '__main__':
    unittest.main()
