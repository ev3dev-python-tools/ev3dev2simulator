import unittest

from ev3dev2.sound import Sound

class SoundTest(unittest.TestCase):
    def test_something(self):
        spkr = Sound()
        # Play 'bark.wav':
        # spkr.play_file('inputFiles/bark.wav')

        spkr.play_note("C4", 0.5)
        spkr.play_note("D4", 0.5)
        spkr.play_note("E4", 0.5)
        spkr.play_note("C4", 0.5)
        spkr.play_note("C4", 0.5)
        spkr.play_note("D4", 0.5)
        spkr.play_note("E4", 0.5)
        spkr.play_note("C4", 0.5)
        spkr.play_note("E4", 0.5)
        spkr.play_note("F4", 0.5)
        spkr.play_note("G4", 0.5)


if __name__ == '__main__':
    unittest.main()
