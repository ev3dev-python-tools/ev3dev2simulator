import unittest
from math import pi
from unittest.mock import patch, MagicMock

from pymunk.vec2d import Vec2d

from ev3dev2simulator.config.config import load_config
from ev3dev2simulator.state.RobotState import RobotState

load_config(None)


class TestRobotState(unittest.TestCase):

    @staticmethod
    def default_config():
        return {'center_x': 0,
                'center_y': 0,
                'orientation': 180,
                'name': 'test_bot',
                'parts': [
                    {
                        'name': 'brick-left',
                        'type': 'brick',
                        'brick': '0',
                        'x_offset': '-39',
                        'y_offset': '-22.5'},
                    {
                        'name': 'motor-left',
                        'type': 'motor',
                        'x_offset': '-60',
                        'y_offset': '0.01',
                        'brick': '0',
                        'port': 'ev3-ports:outA'
                    },
                    {
                        'name': 'motor-right',
                        'type': 'motor',
                        'x_offset': '60',
                        'y_offset': '0.01',
                        'brick': '0',
                        'port': 'ev3-ports:outD'
                    },
                    {
                        'name': 'measurement-probe',
                        'type': 'arm',
                        'x_offset': '15',
                        'y_offset': '102',
                        'brick': '0',
                        'port': 'ev3-ports:outB'
                    },
                    {
                        'name': 'ultrasonic-sensor-rear',
                        'type': 'ultrasonic_sensor',
                        'x_offset': 0,
                        'y_offset': -145,
                        'direction': 'bottom',
                        'brick': 0,
                        'port': 'ev3-ports:in4'
                    }
                ]
                }

    def test_load_robot_config(self):
        with patch('ev3dev2simulator.state.RobotState.get_robot_config') as get_robot_config_mock:
            get_robot_config_mock.return_value = {
                'parts': [
                    {
                        'name': 'brick-left',
                        'type': 'brick',
                        'brick': '0',
                        'x_offset': '-39',
                        'y_offset': '-22.5'
                    }
                ]
            }
            state = RobotState(self.default_config())
            self.assertEqual(len(state.parts), 4 + 1 + 2 + 1)  # 4 sensors/actuators + 1 brick + 2 leds + 1 speaker
            config = {
                'center_x': 0,
                'center_y': 0,
                'orientation': 180,
                'name': 'test_bot',
                'type': 'test_robot'
            }
            state = RobotState(config)
            self.assertEqual(4, len(state.parts))  # only a brick



    def test_setup_pymunk_shapes(self):
        state = RobotState(self.default_config())
        state.setup_pymunk_shapes(1)
        self.assertEqual(state.wheel_distance, 120)
        self.assertEqual(len(state.shapes), 4 + 1 + 2 + 1)  # 4 sensors/actuators + 1 brick + 2 leds + 1 speaker
        self.assertEqual(state.body.angle, pi)

        config_with_one_wheel = self.default_config().copy()
        del config_with_one_wheel['parts'][1]
        config_with_one_wheel['parts'].append({
            'name': 'invalid_sensor',
            'type': 'type_that_does_not_exist',
        })
        state = RobotState(config_with_one_wheel)
        self.assertRaises(RuntimeError, state.setup_pymunk_shapes, 1)

    def test_reset(self):
        state = RobotState(self.default_config())
        state.setup_pymunk_shapes(1)
        for arm in state.side_bar_sprites:
            arm.rotate_x = 0  # this is set in setup visuals
            arm.rotate_y = 0  # this is set in setup visuals
        x = state.x * state.scale
        y = state.y * state.scale
        state.body.position = Vec2d(5, 5)  # 5 per sec
        state._move_position(Vec2d(5, 5))
        self.assertEqual(state.body.position, Vec2d(5, 5))
        self.assertEqual(state.body.velocity, Vec2d(5 * 30, 5 * 30))

        state.reset()

        self.assertEqual(state.body.position, Vec2d(x, y))
        self.assertEqual(state.body.velocity, Vec2d(0, 0))

    def test_execute_movement(self):
        state = RobotState(self.default_config())
        state.setup_pymunk_shapes(1)
        for arm in state.side_bar_sprites:
            arm.rotate_x = 0  # this is set in setup visuals
            arm.rotate_y = 0  # this is set in setup visuals
        state.execute_movement(5, 5)
        self.assertAlmostEqual(tuple(state.body.velocity)[0], 0.0, 3)  # no x movement
        self.assertAlmostEqual(tuple(state.body.velocity)[1], -5.0 * 30, 3)  # -150 y distance per second
        self.assertEqual(state.body.angle, pi)

    def test_arm_movement(self):
        config = self.default_config().copy()
        config['parts'].append({
            'name': 'measurement-probe',
            'type': 'arm',
            'x_offset': 15,
            'y_offset': 102,
            'brick': 0,
            'port': 'ev3-ports:outB'
        })

        with patch('ev3dev2simulator.robotpart.Arm.ArmLarge') as ArmLargeMock:
            arm_instance = ArmLargeMock.return_value
            state = RobotState(self.default_config())
            state.setup_pymunk_shapes(1)

            state.execute_arm_movement((0, 'ev3-ports:outB'), 15)
            state.actuators[(0, 'ev3-ports:outB')].side_bar_arm.degrees = 15

            self.assertEqual(len(arm_instance.mock_calls), 3)  # first two have to do with a sprite list
            fn_name, args, kwargs = arm_instance.mock_calls[2]
            self.assertEqual(fn_name, 'rotate')
            self.assertEqual(args, (15,))

    def test_set_obstacles(self):
        config = self.default_config().copy()
        config['parts'].append({
            'name': 'color_test_sensor',
            'type': 'color_sensor',
            'x_offset': 0,
            'y_offset': 81,
            'brick': 0,
            'port': 'ev3-ports:in2'
        })

        config['parts'].append({
            'name': 'touch_test_sensor',
            'type': 'touch_sensor',
            'side': 'left',
            'x_offset': 0,
            'y_offset': -81,
            'brick': 0,
            'port': 'ev3-ports:in3'
        })
        state = RobotState(config)
        state.setup_pymunk_shapes(1)
        for arm in state.side_bar_sprites:
            arm.rotate_x = 0  # this is set in setup visuals

        color_obstacle_mock = MagicMock()
        rock_mock = MagicMock()
        lake_mock = MagicMock()

        state.set_color_obstacles([color_obstacle_mock])
        state.set_touch_obstacles([rock_mock])
        state.set_falling_obstacles([lake_mock])

        self.assertEqual(state.sensors[(0, 'ev3-ports:in3')].sensible_obstacles, [rock_mock])
        self.assertEqual(state.sensors[(0, 'ev3-ports:in2')].sensible_obstacles, [color_obstacle_mock])
        self.assertEqual(state.sensors[(0, 'ev3-ports:in4')].sensible_obstacles, [lake_mock])
        self.assertEqual(state.actuators[(0, 'ev3-ports:outA')].sensible_obstacles, [lake_mock])

    def test_setters_getters(self):
        state = RobotState(self.default_config())
        state.setup_pymunk_shapes(1)

        self.assertEqual(len(state.get_shapes()), 4 + 1 + 2 + 1)
        self.assertEqual(state.get_sensor((0, 'ev3-ports:in4')).get_ev3type(), 'ultrasonic_sensor')
        self.assertEqual(state.get_bricks()[0].name, 'brick-left')
        self.assertEqual(len(state.get_sensors()), 1)
        self.assertEqual(state.get_anchor().name, 'brick-left')
        del state.bricks[0]
        self.assertEqual(state.get_anchor(), None)

if __name__ == '__main__':
    unittest.main()
