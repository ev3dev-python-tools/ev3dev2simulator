import unittest

from ev3dev2.sound import Sound

class SoundTest(unittest.TestCase):
    def test_something(self):
        spkr = Sound()
        # Play 'bark.wav':
        spkr.play_file('inputFiles/bark.wav')

        spkr.play_note()

if __name__ == '__main__':
    unittest.main()
