import unittest
from unittest.mock import MagicMock

from ev3dev2simulator.state.RobotState import RobotState
from ev3dev2simulator.visualisation.Sidebar import Sidebar
from tests.ev3dev2.simulator.state.test_RobotState import TestRobotState

class MyTestCase(unittest.TestCase):
    def test_add_robot(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)

        sidebar = Sidebar(100, 150, 200, 300)
        sidebar_sprite_mock = MagicMock()
        sidebar.init_robot(state.name, state.sensors, state.get_bricks(), [sidebar_sprite_mock])

        self.assertEqual(len(sidebar.robot_info), 1)

    def test_add_robot_info(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)

        sidebar = Sidebar(100, 150, 200, 300)
        sidebar_sprite_mock = MagicMock()
        state.values[(0, 'ev3-ports:in4')] = 5
        state.sounds[(0, 'speaker')] = 'test_sound'
        sidebar.init_robot(state.name, state.sensors, state.get_bricks(), [sidebar_sprite_mock])

        sidebar.add_robot_info(state.name, state.values, state.sounds)
        self.assertEqual(sidebar.robot_info[state.name][(0, 'ev3-ports:in4')]['value'], 5)
        self.assertEqual(sidebar.robot_info[state.name][(0, 'speaker')]['value'], 'test_sound')


if __name__ == '__main__':
    unittest.main()
