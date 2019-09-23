import json
import socket
from typing import Any

from ev3dev2.connection import MotorCommand, DataRequest


class ClientSocket:
    """
    Class responsible for the establishing and maintaining the socket connection with the simulator.
    This connection is a TCP stream.
    """


    def __init__(self):
        self.client = None


    def setup(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 6840))


    def send_motor_command(self, command: MotorCommand):
        """
        Serialise and send the given MotorCommand to the simulator.
        :param command: to send.
        """

        jsn = self._serialize(command)
        self.client.send(jsn)


    def send_data_request(self, request: DataRequest) -> Any:
        """
        Serialise and send the given DataRequest to the simulator.
        Block while waiting for an answer. Return the answer when received.
        :param request: to send.
        :return: the answer to the given request.
        """

        jsn = self._serialize(request)
        self.client.send(jsn)

        while True:
            val = self.client.recv(32)

            if val:
                return val


    def _serialize(self, message) -> bytes:
        """
        Serialize the given message so it can be send via a stream channel.
        :param message: to be serialized.
        :return: bytes representing the message.
        """

        obj_dict = message.serialize()
        jsn = json.dumps(obj_dict)
        jsn = jsn.ljust(128, '#')

        return str.encode(jsn)


client_socket = ClientSocket()


def get_client_socket() -> ClientSocket:
    return client_socket
