"""
The module sound_command contains the dataclass SoundCommand.
"""
from dataclasses import dataclass

from ev3dev2simulator.connection.message.command import Command


@dataclass
class SoundCommand(Command):
    """
    Command send from the ev3dev2 mock to the simulator telling the robot to display the supplied message.
    """

    def __init__(self, message: str, duration: float, sound_type: str):
        self.message = message
        self.duration = duration
        self.sound_type = sound_type

    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """

        return {
            'type': 'SoundCommand',
            'duration': self.duration,
            'message': self.message,
            'soundType': self.sound_type
        }
