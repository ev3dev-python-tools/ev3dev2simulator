from abc import ABC, abstractmethod


class MotorCommand(ABC):
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

        pass
