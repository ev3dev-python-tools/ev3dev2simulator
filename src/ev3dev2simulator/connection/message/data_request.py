"""
The module data_request contains the dataclass DataRequest.
"""

from dataclasses import dataclass

from ev3dev2simulator.connection.message.command import Command


@dataclass
class DataRequest(Command):
    """
    DataRequest object are used to request the latest value of a sensor attached to the given address.
    """
    def __init__(self, address: str):
        self.address = address

    def serialize(self) -> dict:
        return {'type': 'DataRequest', 'address': self.address}
