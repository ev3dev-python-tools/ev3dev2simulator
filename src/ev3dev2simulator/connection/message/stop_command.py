"""
The module stop_command contains the dataclass StopCommand.
"""

from dataclasses import dataclass
from ev3dev2simulator.connection.message.motor_command import MotorCommand


@dataclass
class StopCommand(MotorCommand):
    """
    Command send from the ev3dev2 mock to the simulator telling the motor with the supplied address to stop.
    This command also includes the current speed of the motor in degrees per second and a stop action, determining
    how the motor should stop. This can be 'hold', 'break' or 'coast'.
    """
    # NOTE: error with pylint
    # pylint: disable=useless-super-delegation
    def __init__(self, address, speed, stop_action):
        super().__init__(address, speed, stop_action)

    def serialize(self) -> dict:
        return {
            'type': 'StopCommand',
            'address': self.address,
            'speed': self.speed,
            'stop_action': self.stop_action
        }
