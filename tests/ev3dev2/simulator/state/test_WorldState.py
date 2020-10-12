import unittest

from ev3dev2simulator.config.config import load_config
from ev3dev2simulator.state.world_state import WorldState

load_config(None)

class TestWorldState(unittest.TestCase):

    def default_config(self):
        return {
            'board_height': 1273,
            'board_width': 1273,
            'board_color': [59, 60, 54],
            'robots': [{
                'center_x': 0,
                'center_y': 0,
                'orientation': 180,
                'name': 'test_bot',
                'parts': [
                    {
                        'name': 'brick-left',
                        'type': 'brick',
                        'brick': 0,
                        'x_offset': -39,
                        'y_offset': -22.5
                    },
                    {
                        'name': 'motor-left',
                        'type': 'motor',
                        'x_offset': -60,
                        'y_offset': 0.01,
                        'brick': 0,
                        'port': 'ev3-ports:outA'
                    },
                    {
                        'name': 'motor-right',
                        'type': 'motor',
                        'x_offset': 60,
                        'y_offset': 0.01,
                        'brick': 0,
                        'port': 'ev3-ports:outD'
                    },
                ]}
            ],
            'obstacles': [
                {
                    'name': 'rock1',
                    'x': 825,
                    'y': 1050,
                    'width': 150,
                    'height': 60,
                    'color': [169, 169, 169],
                    'angle': 10,
                    'type': 'rock'
                },
                {
                    'name': 'lake_red',
                    'border_width': 29,
                    'inner_radius': 38,
                    'color': [201, 45, 57],
                    'x': 397,
                    'y': 232,
                    'type': 'lake'
                },
                {
                    'name': 'bottle',
                    'x': 1000,
                    'y': 300,
                    'radius': 60,
                    'color': [85, 107, 47],
                    'type': 'bottle'
                }
            ]
        }

    def test_constructor(self):
        config = self.default_config()
        config['obstacles'].append({'type': 'invalid_type'})
        world_state = WorldState(config)
        self.assertEqual(len(world_state.get_robots()), 1)
        self.assertEqual(len(world_state.obstacles), 2)
        self.assertEqual(len(world_state.static_obstacles), 3)  # lake + board + edge
        self.assertEqual(world_state.board_width, 1273)
        self.assertEqual(world_state.board_height, 1273)

    def test_reset(self):
        world_state = WorldState(self.default_config())
        world_state.setup_pymunk_shapes(1)
        bottle = world_state.obstacles[1]
        orig_pos = bottle.body.position
        bottle.body.position = (5, 5)
        self.assertEqual(bottle.body.position, (5, 5))
        world_state.reset()
        self.assertEqual(bottle.body.position, orig_pos)

    def test_setup_pymunk_shapes(self):
        world_state = WorldState(self.default_config())
        world_state.setup_pymunk_shapes(0.5)
        self.assertEqual(len(world_state.space.bodies), 3)  # 1 robot + 1 bottle + 1 rock
        bottle = world_state.obstacles[1]
        self.assertEqual(bottle.body.position, (500, 150))


    def test_set_object_at_position_as_selected(self):
        world_state = WorldState(self.default_config())
        world_state.setup_pymunk_shapes(0.5)
        self.assertEqual(len(world_state.space.bodies), 3)  # 1 robot + 1 bottle + 1 rock
        bottle = world_state.obstacles[1]
        self.assertEqual(bottle.body.position, (500, 150))

        world_state.set_object_at_position_as_selected((500, 150))
        self.assertEqual(world_state.selected_object, bottle.body)
        world_state.unselect_object()
        self.assertEqual(world_state.selected_object, None)
        world_state.set_object_at_position_as_selected((25000, 25000))  # this should not exist
        self.assertEqual(world_state.selected_object, None)





if __name__ == '__main__':
    unittest.main()
