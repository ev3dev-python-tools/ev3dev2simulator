from typing import Any

from ev3dev2.connection.ClientSocket import get_client_socket
from ev3dev2.connection.DataRequest import DataRequest
from ev3dev2.util.Singleton import Singleton


class SensorConnector(metaclass=Singleton):
    """
    The SensorConnector class provides a translation layer between the raw sensor classes
    and the sensors on the actual robot. This includes sensor data.
    This class is responsible for creating DataRequests to be send to simulator.
    """


    def __init__(self):
        self.client_socket = get_client_socket()


    def get_value(self, address: str) -> Any:
        """
        Get data of the simulated sensor at the given address.
        :param address: of the sensor.
        """

        request = DataRequest(address)
        return self.client_socket.send_data_request(request)
