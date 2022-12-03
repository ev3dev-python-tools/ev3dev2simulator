"""
The module rotate_command contains the dataclass RotateCommand.
"""
from dataclasses import dataclass

from ev3dev2simulator.connection.message.motor_command import MotorCommand


@dataclass
class RotateCommand(MotorCommand):
    """
    Command send from the ev3dev2 mock to the simulator telling the motor with the supplied address to rotate.
    This is done at the given speed in degrees per second for the given distance in degrees.
    The command also includes a stop action determining how to motor should stop when it is done rotating.
    This can be 'hold', 'brake' or 'coast'.

    Coast means that power will be removed from the motor and it will freely coast to a stop. Brake means
    that power will be removed from the motor and a passive electrical load will be placed on the motor.
    This is usually done by shorting the motor terminals together. This load will absorb the energy from the
    rotation of the motors and cause the motor to stop more quickly than coasting. hold does not remove
    power from the motor. Instead, it actively tries to hold the motor at the current position. If an external
    force tries to turn the motor, the motor will ‘push back’ to maintain its position.

    The simulator simulates coasting, but implements 'brake' and 'hold' just by a direct stop in the simulator.

    """

    def __init__(self,
                 address: str,
                 speed: float,
                 distance: float,
                 stop_action: str):
        super(RotateCommand, self).__init__(address, speed, stop_action)
        self.distance = distance

    def serialize(self) -> dict:
        return {
            'type': 'RotateCommand',
            'address': self.address,
            'speed': self.speed,
            'distance': self.distance,
            'stop_action': self.stop_action
        }
