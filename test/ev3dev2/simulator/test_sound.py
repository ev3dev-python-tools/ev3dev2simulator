import sys
import unittest
from time import sleep

from unittest.mock import patch, MagicMock

clientSocketModuleMock = MagicMock()
sys.modules['ev3dev2simulator.connection.ClientSocket'] = clientSocketModuleMock
# you cannot import ClientSocket, since that sets up a connection

clientSocketMock = MagicMock()
clientSocketModuleMock.get_client_socket = lambda: clientSocketMock

from ev3dev2.sound import Sound


class SoundTest(unittest.TestCase):

    def tearDown(self):
        clientSocketMock.reset_mock()

    def test_beep(self):
        spkr = Sound()
        spkr.beep(play_type=1)
        spkr.beep(play_type=0)

        self.assertEqual(len(clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(), {'type': 'SoundCommand', 'duration': 0.2, 'message': 'playing note with frequency: 440.0', 'soundType': 'note'})

    def test_play_tone(self):
        spkr = Sound()
        spkr.play_tone(500, duration=0.3, volume=50, play_type=1)
        sleep(0.3)  # prevents call order switches
        spkr.play_tone(1500, duration=0.4, volume=50, play_type=0)

        self.assertEqual(len(clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.3, 'message': 'playing note with frequency: 500',
                              'soundType': 'note'})

        fn_name, args, kwargs = clientSocketMock.mock_calls[1]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.4, 'message': 'playing note with frequency: 1500',
                              'soundType': 'note'})

    def test_tone(self):
        spkr = Sound()
        spkr.tone([
            (392, 350, 100), (492, 350), (292,), ()
        ])

        self.assertEqual(len(clientSocketMock.mock_calls), 4)

        fn_name, args, kwargs = clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.350, 'message': 'playing note with frequency: 392',
                              'soundType': 'note'})

        fn_name, args, kwargs = clientSocketMock.mock_calls[1]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.350, 'message': 'playing note with frequency: 492',
                              'soundType': 'note'})

        fn_name, args, kwargs = clientSocketMock.mock_calls[2]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.2, 'message': 'playing note with frequency: 292',
                              'soundType': 'note'})

        fn_name, args, kwargs = clientSocketMock.mock_calls[3]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.2, 'message': 'playing note with frequency: 440.0',
                              'soundType': 'note'})

    def test_play_note(self):
        spkr = Sound()
        spkr.play_note("C4", 0.5)
        spkr.play_note("D4", 0.3)
        spkr.play_note("E4", 0.01)

        self.assertEqual(len(clientSocketMock.mock_calls), 3)

        fn_name, args, kwargs = clientSocketMock.mock_calls[2]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.01, 'message': 'playing note with frequency: 330',
                              'soundType': 'note'})
    #
    #
    def test_play_song(self):
        spkr = Sound()
        spkr.play_song((
            ('G4', 'h'),  # meas 1
            ('D5', 'h'),
            ('C5', 'e3'),  # meas 2
            ('B4', 'e3'),
            ('A4', 'e3'),
            ('G5', 'h'),
            ('D5', 'q'),
        ), tempo=150)

        self.assertEqual(len(clientSocketMock.mock_calls), 7)

        fn_name, args, kwargs = clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.8, 'message': 'playing note with frequency: 392',
                              'soundType': 'note'})

        fn_name, args, kwargs = clientSocketMock.mock_calls[2]
        self.assertEqual(fn_name, 'send_sound_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.13333333333333333, 'message': 'playing note with frequency: 165',
                              'soundType': 'note'})
    #
    # def test_play_file(self):
    #     spkr = Sound()
    #     spkr.play_file('inputFiles/bark.wav', play_type=0)
    #
    #     # Test for invalid path files
    #     with self.assertRaises(ValueError) as cm:
    #         spkr.play_file('file/that/does/not/exist.wav', play_type=0)
    #
    #     self.assertEqual(cm.exception.args[0], 'file/that/does/not/exist.wav does not exist')
    #
    #     # Test for wrong extensions
    #     with self.assertRaises(ValueError) as cm:
    #         spkr.play_file('inputFiles/bark', play_type=0)
    #
    #     self.assertEqual(cm.exception.args[0], 'invalid sound file (inputFiles/bark), only .wav files are supported')
    #
    # def test_speak(self):
    #     spkr = Sound()
    #     spkr.speak("test test test test test", volume=100, play_type=1)
    #     spkr.play_note("C4", 2)
    #     spkr.speak("kekeroni", volume=100, play_type=0)


if __name__ == '__main__':
    unittest.main()
