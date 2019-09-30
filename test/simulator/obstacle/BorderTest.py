import unittest

import arcade

from simulator.obstacle.Border import Border
from simulator.util.Util import load_config


class BorderTest(unittest.TestCase):

    def test_create_border(self):
        cfg = load_config()

        border = Border(cfg, arcade.color.WHITE)

        # based on screen_with: 863, screen_height: 863, edge_spacing: 15
        top = [(15.0, 838.0), (15.0, 848.0), (848.0, 848.0), (848.0, 838.0)]
        right = [(838.0, 15.0), (838.0, 848.0), (848.0, 848.0), (848.0, 15.0)]
        bottom = [(15.0, 15.0), (15.0, 25.0), (848.0, 25.0), (848.0, 15.0)]
        left = [(15.0, 15.0), (15.0, 848.0), (25.0, 848.0), (25.0, 15.0)]

        self.assertEqual(border.top_points, top)
        self.assertEqual(border.right_points, right)
        self.assertEqual(border.bottom_points, bottom)
        self.assertEqual(border.left_points, left)


if __name__ == '__main__':
    unittest.main()
