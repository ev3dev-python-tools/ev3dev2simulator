import unittest
from unittest.mock import MagicMock

from ev3dev2simulator.state.robot_simulator import RobotSimulator
from ev3dev2simulator.state.robot_state import RobotState
from tests.ev3dev2.simulator.state.test_RobotState import TestRobotState


class TestRobotSimulator(unittest.TestCase):
    def test_constructor_and_reset(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        state.setup_pymunk_shapes(1)
        for arm in state.side_bar_sprites:
            arm.rotate_x = 0  # this is set in setup visuals
            arm.rotate_y = 0  # this is set in setup visuals
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
        for arm in state.side_bar_sprites:
            arm.rotate_x = 0  # this is set in setup visuals
            arm.rotate_y = 0  # this is set in setup visuals
        sim = RobotSimulator(state)
        sim._sync_physics_sprites = MagicMock()
        val = sim.get_value((0, 'ev3-ports:in4'))
        self.assertEqual(val, 2550)
        self.assertEqual(sim.locks[(0, 'ev3-ports:in4')].locked(), True)
        sim.update()
        self.assertEqual(sim.locks[(0, 'ev3-ports:in4')].locked(), False)

    def test_determine_port(self):
        conf = TestRobotState.default_config()
        state = RobotState(conf)
        sim = RobotSimulator(state)

        # nothing given
        kwargs = {}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'dev_not_connected')

        # no class given
        kwargs = {'address': 'ev3-ports:in4'}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'dev_not_connected')

        # single class and address given
        kwargs = {'address': 'ev3-ports:in4', 'driver_name': 'lego-ev3-us'}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'ev3-ports:in4')

        # single class and address given but wrong driver_name given ('lego-ev3-touch' instead of 'lego-ev3-us')
        kwargs = {'address': 'ev3-ports:in4', 'driver_name': 'lego-ev3-touch'}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'dev_not_connected')

        # single class and None address given
        kwargs = {'address': None, 'driver_name': 'lego-ev3-us'}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'ev3-ports:in4')

        # multiple classes and address given
        kwargs = {'address': 'ev3-ports:outA', 'driver_name': ['lego-ev3-l-motor', 'lego-nxt-motor']}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'ev3-ports:outA')

        # single class and invalid address given
        kwargs = {'address': 'ev3-ports:in3', 'driver_name': 'lego-ev3-us'}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'dev_not_connected')

        # multiple classes and invalid address given
        kwargs = {'address': 'ev3-ports:outC', 'driver_name': ['lego-ev3-l-motor', 'lego-nxt-motor']}
        port = sim.determine_port(0, kwargs, '')
        self.assertEqual(port, 'dev_not_connected')

        # leds
        kwargs = {'address': None, 'driver_name': None}
        port = sim.determine_port(0, kwargs, 'leds')
        self.assertEqual(port, 'leds_addr')

if __name__ == '__main__':
    unittest.main()
