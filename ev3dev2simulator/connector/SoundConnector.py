from time import sleep
from typing import Any

# from ev3dev2simulator.connection.ClientSocket import get_client_socket
# from ev3dev2simulator.connection.message.SoundCommand import SoundCommand

import simpleaudio as sa
import pyttsx3 as tts
import numpy as np


class SoundConnector:
    """
    The SoundConnector class provides a translation layer between the ev3dev2 Sound classes
    and the simulated robot.
    This class is responsible for creating SoundCommands to be send to simulator.
    """

    def __init__(self):
        # self.client_socket = get_client_socket()
        pass

    def play_file(self, file_url: str, blocking: bool = True):
        print("load")
        wave_obj = sa.WaveObject.from_wave_file(file_url)
        play_obj = wave_obj.play()
        if blocking:
            play_obj.wait_done()  # Wait until sound has finished playing
        # command = SoundCommand(message)
        # return self.client_socket.send_sound_command(command)

    def play_tone_sequence(self, *args) -> Any:
        argList = list(args[0])[0]
        for lst in argList:
            print(lst)
            frequency = lst[0]
            duration = float(lst[1] / 1000.0)
            delay = lst[2]
            """
            Create and send a SoundCommand to be send to the simulator with the given text to speak.
            """

            fs = 44100  # 44100 samples per second
            t = np.linspace(0, duration, duration * fs, False)
            note = np.sin(frequency * t * 2 * np.pi)

            print(note)
            # Ensure that highest value is in 16-bit range
            audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
            # Convert to 16-bit data
            audio = audio.astype(np.int16)

            # Start playback
            play_obj = sa.play_buffer(audio, 1, 2, fs)

            # Wait for playback to finish before exiting

            play_obj.wait_done()

            # command = SoundCommand(message)
            # return self.client_socket.send_sound_command(command)
            sleep(delay / 1000.0)



    def speak(self, text, espeak_opts, desired_volume, play_type):
        try:
            engine = tts.init()
        except OSError:
            print("Please make sure you have installed the required text to speech library such as espeak for Linux")

        engine.setProperty('volume', desired_volume / 100.0)

        engine.say(text)
        engine.runAndWait()

        # command = SoundCommand(message)
        # return self.client_socket.send_sound_command(command)
