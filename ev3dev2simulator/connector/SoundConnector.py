from typing import Any

from ev3dev2simulator.connection.ClientSocket import get_client_socket
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand


class SoundConnector:
    """
    The SoundConnector class provides a translation layer between the ev3dev2 Sound classes
    and the simulated robot.
    This class is responsible for creating SoundCommands to be send to simulator.
    """


    def __init__(self):
        self.client_socket = get_client_socket()


    def speak(self, message: str) -> Any:
        """
        Create and send a SoundCommand to be send to the simulator with the given text to speak.
        """

        command = SoundCommand(message)
        return self.client_socket.send_sound_command(command)
