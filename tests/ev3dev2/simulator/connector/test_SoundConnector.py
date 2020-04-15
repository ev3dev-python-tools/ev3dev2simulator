import sys
import unittest
from time import sleep

from unittest.mock import MagicMock, patch

from ev3dev2.sound import Sound

class SoundTest(unittest.TestCase):

    def setUp(self) -> None:
        self.DeviceMockPatcher = patch('ev3dev2.DeviceConnector')
        self.get_client_socketPatcher = patch('ev3dev2simulator.connector.SoundConnector.get_client_socket')

        self.DeviceMockPatcher.start()
        self.get_client_socketMock = self.get_client_socketPatcher.start()

        self.addCleanup(self.DeviceMockPatcher.stop)
        self.addCleanup(self.get_client_socketPatcher.stop)

        self.clientSocketMock = MagicMock()
        self.get_client_socketMock.return_value = self.clientSocketMock

    def test_beep(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.beep(play_type=1)
        spkr.beep(play_type=0)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.2, 'message': 'Playing note with frequency: 440.0',
                              'soundType': 'note'})

    def test_play_tone(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.play_tone(500, duration=0.3, volume=50, play_type=1)
        sleep(0.3)  # prevents call order switches
        spkr.play_tone(1500, duration=0.4, volume=50, play_type=0)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)
        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.3, 'message': 'Playing note with frequency: 500',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.4, 'message': 'Playing note with frequency: 1500',
                              'soundType': 'note'})

    def test_tone(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.tone([
            (392, 350, 100), (492, 350), (292,), ()
        ])

        self.assertEqual(len(self.clientSocketMock.mock_calls), 4)

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.350, 'message': 'Playing note with frequency: 392',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.350, 'message': 'Playing note with frequency: 492',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[2]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.2, 'message': 'Playing note with frequency: 292',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[3]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.2, 'message': 'Playing note with frequency: 440.0',
                              'soundType': 'note'})

    def test_play_note(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.play_note("C4", 0.5)
        spkr.play_note("D4", 0.3)
        spkr.play_note("E4", 0.01)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 3)

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[2]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.01, 'message': 'Playing note with frequency: 330',
                              'soundType': 'note'})

    def test_play_song(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.play_song((
            ('G4', 'h'),  # meas 1
            ('D5', 'h'),
            ('C5', 'e3'),  # meas 2
            ('B4', 'e3'),
            ('A4', 'e3'),
            ('G5', 'h'),
            ('D5', 'q'),
        ), tempo=150)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 7)

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.8, 'message': 'Playing note with frequency: 392',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[1]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 0.8, 'message': 'Playing note with frequency: 587',
                              'soundType': 'note'})

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[2]
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': (0.8/4) * 2/3,  # a triplet
                              'message': 'Playing note with frequency: 523',
                              'soundType': 'note'})

    def test_play_file(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.play_file('inputFiles/bark.wav', play_type=0)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 1)

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]

        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 3.0,
                              'message': 'Playing file: ``inputFiles/bark.wav``',
                              'soundType': 'file'})

        # Test for invalid path files
        with self.assertRaises(ValueError) as cm:
            spkr.play_file('file/that/does/not/exist.wav', play_type=0)

        self.assertEqual(cm.exception.args[0], 'file/that/does/not/exist.wav does not exist')

        # Test for wrong extensions
        with self.assertRaises(ValueError) as cm:
            spkr.play_file('inputFiles/bark', play_type=0)

        self.assertEqual(cm.exception.args[0], 'invalid sound file (inputFiles/bark), only .wav files are supported')


    def test_speak(self):
        spkr = Sound()
        spkr.connector.play_actual_sound = False
        spkr.speak("tests tests tests tests tests", volume=100, play_type=1)
        spkr.speak("kekeroni", volume=100, play_type=0)

        self.assertEqual(len(self.clientSocketMock.mock_calls), 2)

        fn_name, args, kwargs = self.clientSocketMock.mock_calls[0]
        self.assertEqual(fn_name, 'send_command')
        self.assertDictEqual(args[0].serialize(),
                             {'type': 'SoundCommand', 'duration': 1.5,  # 200 words per minute, (5 / 200) * 60 = 1.5
                              'message': 'Saying: ``tests tests tests tests tests``',
                              'soundType': 'speak'})

if __name__ == '__main__':
    unittest.main()
