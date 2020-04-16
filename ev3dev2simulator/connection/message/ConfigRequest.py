from ev3dev2simulator.connection.message.Command import Command


class ConfigRequest(Command):
    """
    ConfigRequest objects are used to request the config of a sensor to determine its port.
    Based on the type of the part, the first occurrence of the type found in the configuration will be returned.
    """
    def __init__(self, kwargs: str):
        self.kwargs = kwargs

    def serialize(self) -> dict:
        return {'type': 'ConfigRequest', 'kwargs': self.kwargs}
