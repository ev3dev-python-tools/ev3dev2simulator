import unittest

from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connector.MotorCommandCreator import MotorCommandCreator


class MotorCommandCreatorTest(unittest.TestCase):

    def test_frames_required(self):
        creator = MotorCommandCreator()

        frames = creator._frames_required(20, 100)
        self.assertEqual(frames, 150)

        frames = creator._frames_required(20, -100)
        self.assertEqual(frames, 150)

        frames = creator._frames_required(33, 1000)
        self.assertEqual(frames, 909)

        frames = creator._frames_required(-33, 1000)
        self.assertEqual(frames, 909)

        frames = creator._frames_required(-66, -700)
        self.assertEqual(frames, 318)


    def test_coast_frames_required(self):
        coasting_sub = load_config()['wheel_settings']['coasting_subtraction']
        creator = MotorCommandCreator()

        frames = creator._coast_frames_required(20)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)

        frames = creator._coast_frames_required(-20)
        self.assertEqual(frames, int(round((20 / coasting_sub))), 5)


    def test_to_pixels_per_frame(self):
        creator = MotorCommandCreator()

        ppf = creator._to_pixels_per_frame(100, 730)
        self.assertAlmostEqual(ppf, 3.508, 3)

        ppf = creator._to_pixels_per_frame(100, -730)
        self.assertAlmostEqual(ppf, -3.508, 3)


    def test_to_pixels(self):
        creator = MotorCommandCreator()

        pixels = creator._to_pixels(720)
        self.assertAlmostEqual(pixels, 346, 3)

        pixels = creator._to_pixels(-720)
        self.assertAlmostEqual(pixels, -346, 3)


if __name__ == '__main__':
    unittest.main()
