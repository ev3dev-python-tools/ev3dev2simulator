"""
The module sound_connector contains the classes SimpleAudioError and SoundConnector.
"""


import textwrap
from time import sleep
from typing import Any, Optional
import threading
import wave

import pyttsx3 as tts
import numpy as np
import simpleaudio as sa

from ev3dev2simulator.connection.client_socket import get_client_socket
from ev3dev2simulator.connection.message.sound_command import SoundCommand


class SimpleaudioError(Exception):
    """
    Class representing an error thrown by SimpleAudio
    """


class SoundConnector:
    """
    The SoundConnector class provides a translation layer between the ev3dev2 Sound classes
    and the simulated robot.
    This class is responsible for creating SoundCommands to be send to simulator and playing the sounds locally.
    """

    PLAY_WAIT_FOR_COMPLETE = 0  #: Play the sound and block until it is complete
    PLAY_NO_WAIT_FOR_COMPLETE = 1  #: Start playing the sound but return immediately
    PLAY_LOOP = 2  #: Never return; start the sound immediately after it completes, until the program is killed

    PLAY_TYPES = (
        PLAY_WAIT_FOR_COMPLETE,
        PLAY_NO_WAIT_FOR_COMPLETE,
        PLAY_LOOP
    )

    def __init__(self, play_actual_sound=True):
        self.client_socket = get_client_socket()
        self.play_actual_sound = play_actual_sound

    def _linux_beep(self, tone_sequence) -> Any:
        for tone in tone_sequence:
            frequency = tone.get('frequency', 440.0)  # defaults to 440 hz which is the default of beep
            duration = tone.get('duration', 200) / 1000.0  # defaults to 200 ms which is the default of beep
            delay = tone.get('delay', 100)  # defaults to 100 ms which is the default of beep

            sampling_frequency = 44100
            time_samples = np.linspace(0, duration, int(duration * sampling_frequency), False)
            note = np.sin(frequency * time_samples * 2 * np.pi)

            audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
            audio = audio.astype(np.int16)

            command = SoundCommand("Playing note with frequency: " + str(frequency), duration, "note")
            self.client_socket.send_command(command)

            if self.play_actual_sound:
                try:
                    # Start playback
                    play_obj = sa.play_buffer(audio, 1, 2, sampling_frequency)
                    play_obj.wait_done()
                except SimpleaudioError:
                    print("An error occurred when trying to play a file. Ignoring to keep simulation running")
            sleep(delay / 1000.0)

    def beep(self, args, play_type: int) -> Optional[threading.Thread]:
        """
        Play a tone sequence and send a SoundCommand to the simulator for each tone.
        Based on the Linux Beep command, but with an object as input instead of string arguments

        :param object args: Any additional arguments as list of objects.
            Example: ``[{frequency: 440.0, duration: 200, delay: 100}]``
        :param play_type: The behavior of ``beep`` once playback has been initiated
        :type play_type: ``Sound.PLAY_WAIT_FOR_COMPLETE`` or  ``Sound.PLAY_NO_WAIT_FOR_COMPLETE``
        :return: ``None``
        """

        if play_type == SoundConnector.PLAY_LOOP:
            while True:
                x = threading.Thread(target=self._linux_beep, args=(args,))
                x.start()
                x.join()
        else:
            x = threading.Thread(target=self._linux_beep, args=(args,))
            x.start()

            if play_type == SoundConnector.PLAY_WAIT_FOR_COMPLETE:
                x.join()
            return x

    def play_file(self, wav_file: str, volume: int, play_type: int) -> None:
        """
        Play a wav file and send a SoundCommand to the simulator with the given file url. :param string wav_file: The
        sound file path :param int volume: The play volume, in percent of maximum volume :param play_type: The
        behavior of ``play_file`` once playback has been initiated :type play_type:
        ``SoundConnector.PLAY_WAIT_FOR_COMPLETE``, ``SoundConnector.PLAY_NO_WAIT_FOR_COMPLETE`` or
        ``SoundConnector.PLAY_LOOP`` :return: returns ``None``
        """
        wave_read = wave.open(wav_file, 'rb')
        duration = wave_read.getnframes() / wave_read.getframerate()
        wave_obj = sa.WaveObject.from_wave_read(wave_read)
        wave_read.close()

        command = SoundCommand(f'Playing file: ``{wav_file}``', duration, "file")
        self.client_socket.send_command(command)

        if self.play_actual_sound:
            try:
                play_obj = wave_obj.play()
                if play_type == SoundConnector.PLAY_NO_WAIT_FOR_COMPLETE:
                    return

                play_obj.wait_done()  # Wait until sound has finished playing
                if play_type == SoundConnector.PLAY_LOOP:
                    self.play_file(wav_file, volume, play_type)

            except SimpleaudioError:
                print("An error occurred when trying to play a file. Ignoring to keep simulation running")

    def speak(self, text, espeak_opts, desired_volume: int, play_type: int) -> None:
        """
        Play a text-to-speech file and send a SoundCommand to the simulator with the said text.

        Makes use of the pyttsx3 library.
        - Windows users need to install pypiwin32, installed by: pip install pypiwin32
        - Linux users need to install espeak, installed by: sudo apt-get install espeak
        - Mac users do not need to install any additional software.

        :param string text: The text to speak
        :param string espeak_opts: ``espeak`` command options (advanced usage), NOT IN USE
        :param int desired_volume: The play volume, in percent of maximum volume
        :param play_type: The behavior of ``speak`` once playback has been initiated
        :type play_type: ``Sound.PLAY_WAIT_FOR_COMPLETE``, ``Sound.PLAY_NO_WAIT_FOR_COMPLETE`` or ``Sound.PLAY_LOOP``
        :return: ``None``
        """

        if play_type == SoundConnector.PLAY_LOOP:
            while True:
                self.speak(text, espeak_opts, desired_volume, SoundConnector.PLAY_WAIT_FOR_COMPLETE)

        x = threading.Thread(target=self._tts, args=(text, espeak_opts, desired_volume,), daemon=True)
        x.start()
        if play_type == SoundConnector.PLAY_WAIT_FOR_COMPLETE:
            x.join()

    # noinspection PyUnusedLocal
    def _tts(self, text, _espeak_opts, desired_volume: int) -> None:
        duration = (len(text.split()) / 200) * 60  # based on 200 words per minute as described in the tts docs

        command = SoundCommand(f'Saying: ``{text}``', duration, 'speak')
        self.client_socket.send_command(command)

        if self.play_actual_sound:
            try:
                engine = tts.init()
                engine.setProperty('volume', desired_volume / 100.0)
                engine.say(text)
                engine.runAndWait()
            except OSError as error:
                print(textwrap.dedent('''
                                        Warning, speak could not be executed. Speak makes use of the pyttsx3 library. This requires:
                                        - Windows users to install pypiwin32, installed by: pip install pypiwin32
                                        - Linux users to install espeak, installed by: sudo apt-get install espeak
                                        - Mac users do not need to install any additional software.
                                        '''))
                print('original exception', error)
            except RuntimeError as error:
                print("Warning: 'speak' called before last text-to-speech was handled")
                print(error)
