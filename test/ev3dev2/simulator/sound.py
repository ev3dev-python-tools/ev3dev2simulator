import unittest

from ev3dev2.sound import Sound

class SoundTest(unittest.TestCase):
    def test_play_note(self):
        spkr = Sound()
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

    def test_play_song(self):
        spkr = Sound()
        spkr.play_song((
            ('D4', 'e3'),  # intro anacrouse
            ('D4', 'e3'),
            ('D4', 'e3'),
            ('G4', 'h'),  # meas 1
            ('D5', 'h'),
            ('C5', 'e3'),  # meas 2
            ('B4', 'e3'),
            ('A4', 'e3'),
            ('G5', 'h'),
            ('D5', 'q'),
            ('C5', 'e3'),  # meas 3
            ('B4', 'e3'),
            ('A4', 'e3'),
            ('G5', 'h'),
            ('D5', 'q'),
            ('C5', 'e3'),  # meas 4
            ('B4', 'e3'),
            ('C5', 'e3'),
            ('A4', 'h.'),
        ), tempo=150)

    def test_play_file(self):
        spkr = Sound()
        spkr.play_file('inputFiles/bark.wav')

    def test_speak(self):
        spkr = Sound()
        spkr.speak("test", volume=100)

if __name__ == '__main__':
    unittest.main()
