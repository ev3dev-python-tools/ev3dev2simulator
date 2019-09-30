import socket
import unittest

from ev3dev2.util.MotorCommandCreator import MotorCommandCreator
from simulator.util.Util import load_config


class MotorCommandCreatorTest(unittest.TestCase):

    def setUp(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 6840))
        server.listen(5)


    def test_frames_required(self):
        creator = MotorCommandCreator()

        frames = creator._frames_required(20, 100)
        self.assertEqual(frames, 300)

        frames = creator._frames_required(20, -100)
        self.assertEqual(frames, 300)

        frames = creator._frames_required(33, 1000)
        self.assertEqual(frames, 1818)

        frames = creator._frames_required(-33, 1000)
        self.assertEqual(frames, 1818)

        frames = creator._frames_required(-66, -700)
        self.assertEqual(frames, 636)


    def test_coast_frames_required(self):
        coasting_sub = load_config()['wheel_settings']['coasting_subtraction']
        creator = MotorCommandCreator()

        frames = creator._coast_frames_required(20)
        self.assertEqual(frames, (20 / coasting_sub))

        frames = creator._coast_frames_required(-20)
        self.assertEqual(frames, (20 / coasting_sub))


    def test_to_pixels_per_frame(self):
        creator = MotorCommandCreator()

        ppf = creator._to_pixels_per_frame(100, 730)
        self.assertAlmostEqual(ppf, 2.332, 3)

        ppf = creator._to_pixels_per_frame(100, -730)
        self.assertAlmostEqual(ppf, -2.332, 3)


    def test_to_pixels(self):
        creator = MotorCommandCreator()

        pixels = creator._to_pixels(720)
        self.assertAlmostEqual(pixels, 230)

        pixels = creator._to_pixels(-720)
        self.assertAlmostEqual(pixels, -230)


if __name__ == '__main__':
    unittest.main()
