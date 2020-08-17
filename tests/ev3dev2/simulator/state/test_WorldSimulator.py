import unittest
from unittest.mock import MagicMock

from ev3dev2simulator.config.config import load_config
from ev3dev2simulator.state.world_simulator import WorldSimulator

load_config(None)


class TestWorldSimulator(unittest.TestCase):
    def test_update(self):
        robot_mock = MagicMock()
        world_state_mock = MagicMock()
        world_state_mock.robots = [robot_mock]
        world_simulator = WorldSimulator(world_state_mock)
        world_simulator.robot_simulators[0].update = MagicMock()
        world_simulator.update()
        world_simulator.robot_simulators[0].update.assert_called_once_with()
        self.assertFalse(world_simulator.robot_simulators[0].should_reset)
        world_simulator.request_reset()
        world_simulator.update()
        self.assertEqual(world_simulator.robot_simulators[0].update.call_count, 1)


if __name__ == '__main__':
    unittest.main()
