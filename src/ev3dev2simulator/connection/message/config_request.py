"""
The config_request module contains the class ConfigRequest.
"""

from dataclasses import dataclass

from ev3dev2simulator.connection.message.command import Command


@dataclass
class ConfigRequest(Command):
    """
    ConfigRequest objects are used to request the config of a sensor to determine its port.
    Based on the type of the part, the first occurrence of the type found in the configuration will be returned.
    """
    def __init__(self, kwargs: str, class_name: str):
        self.kwargs = kwargs
        self.class_name = class_name

    def serialize(self) -> dict:
        return {'type': 'ConfigRequest', 'kwargs': self.kwargs, 'class_name': self.class_name}
