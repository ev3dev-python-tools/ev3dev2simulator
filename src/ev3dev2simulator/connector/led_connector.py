"""
The led_connector contains the class LedConnector.
"""

from typing import Any

from ev3dev2simulator.connection.client_socket import get_client_socket
from ev3dev2simulator.connection.message.led_command import LedCommand


class LedConnector:
    """
    The LedConnector class provides a translation layer between the ev3dev2 LED/LEDs classes
    and the LEDs on the simulated robot.
    This class is responsible for creating LedCommands to be send to simulator.
    """

    def __init__(self, address):
        self.address = address
        self.client_socket = get_client_socket()

    def enable(self, brightness: float) -> Any:
        """
        Create a LedCommand to be send to the simulator with the given address of the led to
        be turned on and the brightness to run at.
        """

        command = LedCommand(self.address, brightness)
        return self.client_socket.send_command(command)

    def get_address(self):
        """
        Returns the address of the led.
        """
        return self.address
