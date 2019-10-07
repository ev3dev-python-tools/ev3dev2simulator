from typing import Any

from ev3dev2.simulator.connection.ClientSocket import get_client_socket
from ev3dev2.simulator.connection.message.DataRequest import DataRequest


class SensorConnector:
    """
    The SensorConnector class provides a translation layer between the ev3dev2 sensor classes
    and the sensors on the simulated robot. This includes sensor data.
    This class is responsible for creating DataRequests to be send to simulator.
    """


    def __init__(self, address: str):
        self.address = address
        self.client_socket = get_client_socket()


    def get_value(self) -> Any:
        """
        Get data of the simulated sensor at the given address.
        """

        request = DataRequest(self.address)
        return self.client_socket.send_data_request(request)
