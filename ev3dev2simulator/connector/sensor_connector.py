"""
The module sensor_connector contains the class SensorConnector.
"""

import time
from typing import Any

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.connection.client_socket import get_client_socket
from ev3dev2simulator.connection.message.data_request import DataRequest


class SensorConnector:
    """
    The SensorConnector class provides a translation layer between the ev3dev2 sensor classes
    and the sensors on the simulated robot. This includes sensor data.
    This class is responsible for creating DataRequests to be send to simulator.
    """

    def __init__(self, address: str):
        self.address = address
        if address is None:
            raise RuntimeError('created connector with None as address')

        self.client_socket = get_client_socket()

        self.wait_time = 0.008
        self.frame_time = 1 / int(get_simulation_settings()['exec_settings']['frames_per_second'])
        self.last_request_time = 0

        self.value_cache = None
        self.delta_sum = 0

    def get_value(self) -> Any:
        """
        Get data of the simulated sensor at the given address if required. Provides caching whenever a second request
        would result in the same answer as the first, because they happened in such quick succession that the
        simulator data could not possibly have changed yet. :return: the value in any form of the sensor.
        """

        now = time.time()
        delta = now - self.last_request_time

        self.delta_sum += delta
        self.last_request_time = now

        if delta > self.frame_time or self.delta_sum > self.frame_time:
            self.delta_sum = 0
            self.value_cache = self.send_command()

        else:
            time.sleep(self.wait_time)

        return int(self.value_cache)

    def send_command(self) -> Any:
        """
        Get data of the simulated sensor at the given address.
        :return: the value in any form of the sensor.
        """
        request = DataRequest(self.address)
        return self.client_socket.send_command(request, True)
