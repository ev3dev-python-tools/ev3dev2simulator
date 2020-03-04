from time import sleep
from typing import Any

from ev3dev2simulator.connection.ClientSocket import get_client_socket
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand

import simpleaudio as sa
import pyttsx3 as tts
import numpy as np
import wave

class SoundConnector:
    """
    The SoundConnector class provides a translation layer between the ev3dev2 Sound classes
    and the simulated robot.
    This class is responsible for creating SoundCommands to be send to simulator.
    """

    def __init__(self):
        self.client_socket = get_client_socket()
        pass

    def play_file(self, file_url: str, blocking: bool = True):
        """
        Play a wav file and send a SoundCommand to the simulator with the given file url.
        """
        wave_read = wave.open(file_url, 'rb')
        duration = wave_read.getnframes() / wave_read.getframerate()
        wave_obj = sa.WaveObject.from_wave_read(wave_read)
        wave_read.close()

        command = SoundCommand("playing file: " + file_url, duration, "file")
        self.client_socket.send_sound_command(command)
        try:
            play_obj = wave_obj.play()
            if blocking:
                play_obj.wait_done()  # Wait until sound has finished playing
        except:
            print("An error occurred when trying to play a file. Ignoring to keep simulation running")



    def play_tone_sequence(self, *args) -> Any:
        """
        Play a tone sequence and send a SoundCommand to the simulator for each tone.
        """
        argList = list(args[0])[0]
        for lst in argList:
            frequency = lst[0]
            duration = lst[1] / 1000.0
            delay = lst[2]

            fs = 44100
            t = np.linspace(0, duration, int(duration * fs), False)
            note = np.sin(frequency * t * 2 * np.pi)

            audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
            audio = audio.astype(np.int16)

            command = SoundCommand("playing note with frequency: " + str(fs), duration, "note")
            self.client_socket.send_sound_command(command)

            try:
                # Start playback
                play_obj = sa.play_buffer(audio, 1, 2, fs)
                play_obj.wait_done()
            except:
                print("An error occurred when trying to play a file. Ignoring to keep simulation running")

            sleep(delay / 1000.0)



    def speak(self, text, espeak_opts, desired_volume, play_type):
        """
        Play a text-to-speech file and send a SoundCommand to the simulator with the said text.

        Makes use of the pyttsx3 library.
        - Windows users need to install pypiwin32, installed by: pip install pypiwin32
        - Linux users need to install espeak, installed by: sudo apt-get install espeak
        - Mac users do not need to install any additional software.
        """
        duration = len(text.split()) / 200 * 60  # based on 200 words per minute as described in the tts docs
        try:
            engine = tts.init()
            engine.setProperty('volume', desired_volume / 100.0)

            engine.say(text)
            engine.runAndWait()
        except OSError:
            print("Please make sure you have installed the required text to speech library such as espeak for Linux")

        command = SoundCommand("saying: " + text, duration, 'speak')
        return self.client_socket.send_sound_command(command)
