"""
The module command contains the abstract dataclass Command.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Command(ABC):
    """
    Command send from the ev3dev2 mock to the simulator
    """

    @abstractmethod
    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """
