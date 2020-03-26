import unittest
import arcade

from sys import platform

from ev3dev2simulator.obstacle.Border import Border


class BorderTest(unittest.TestCase):

    def test_create_border(self):
        if platform != "darwin":
            print("currently only executing drawing on macOS")
            return
        arcade.Window(width=5, height=5)
        config = {
            'depth': 15,
            'color': '(255, 255, 255)',
            'type': 'border',
            'outer_spacing': 23
        }

        large_board_height = 1273
        large_board_width = 1273
        scale = 0.60

        border = Border.from_config(large_board_width, large_board_height, config)
        border.create_shape(scale)

        top = [(13.800000000000011, 741.0), (13.800000000000011, 750.0), (750.0, 750.0), (750.0, 741.0)]
        right = [(741.0, 13.800000000000011), (741.0, 750.0), (750.0, 750.0), (750.0, 13.800000000000011)]
        bottom = [(13.800000000000011, 13.799999999999997), (13.800000000000011, 22.799999999999997),
                  (750.0, 22.799999999999997), (750.0, 13.799999999999997)]
        left = [(13.799999999999997, 13.800000000000011), (13.799999999999997, 750.0), (22.799999999999997, 750.0),
                (22.799999999999997, 13.800000000000011)]

        self.assertEqual(border.top_points, top)
        self.assertEqual(border.right_points, right)
        self.assertEqual(border.bottom_points, bottom)
        self.assertEqual(border.left_points, left)


if __name__ == '__main__':
    unittest.main()
