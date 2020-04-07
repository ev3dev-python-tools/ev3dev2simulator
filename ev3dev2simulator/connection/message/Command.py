from abc import ABC, abstractmethod


class Command(ABC):
    """
    Command send from the ev3dev2 mock to the simulator
    """

    @abstractmethod
    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """
        pass
