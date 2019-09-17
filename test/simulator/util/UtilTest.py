import unittest

from simulator.util.Util import get_circle_points, pythagoras


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


if __name__ == '__main__':
    unittest.main()
