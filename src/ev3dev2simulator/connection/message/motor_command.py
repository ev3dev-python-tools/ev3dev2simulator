"""
The module rotate_command contains the dataclass RotateCommand.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ev3dev2simulator.connection.message.command import Command


@dataclass
class MotorCommand(Command, ABC):
    """
    Base class for a motor command sent from the ev3dev2 mock to the simulator.
    """
    def __init__(self,
                 address: str,
                 speed: float,
                 stop_action: str):
        self.address = address
        self.speed = speed
        self.stop_action = stop_action

    @abstractmethod
    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """
