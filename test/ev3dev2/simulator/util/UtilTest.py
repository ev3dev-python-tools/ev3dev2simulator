import unittest

from ev3dev2simulator.util.Util import get_circle_points, calc_differential_steering_angle_x_y, pythagoras


class UtilTest(unittest.TestCase):

    def test_get_circle_points_base(self):
        points = get_circle_points(100, 100, 10)

        self.assertEqual(len(points), 34)


    def test_get_circle_points_diff(self):
        points = get_circle_points(100, 100, 10, 64)

        self.assertEqual(len(points), 66)


    def test_pythagoras(self):
        result = pythagoras(2, 3)
        self.assertAlmostEqual(result, 3.606, 3)


    def test_differential_steering_angle_x_y(self):
        diff_angle, diff_x, diff_y \
            = calc_differential_steering_angle_x_y(10, 2, 3, 0.4)

        self.assertAlmostEqual(diff_angle, 0.1, 3)
        self.assertAlmostEqual(diff_x, 2.194, 3)
        self.assertAlmostEqual(diff_y, 1.199, 3)


if __name__ == '__main__':
    unittest.main()
