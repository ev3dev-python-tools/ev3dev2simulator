from abc import ABC

from ev3dev2simulator.connection.message.Command import Command


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

