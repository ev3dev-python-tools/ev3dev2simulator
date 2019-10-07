import json
import socket
import time
from typing import Any

from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.message import MotorCommand, SoundCommand, DataRequest


class ClientSocket:
    """
    Class responsible for the establishing and maintaining the socket connection with the simulator.
    This connection is a TCP stream.
    """


    def __init__(self):
        port = load_config()['exec_settings']['socket_port']

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', port))

        time.sleep(1)


    def send_motor_command(self, command: MotorCommand):
        """
        Serialise and send the given MotorCommand to the simulator.
        :param command: to send.
        """

        jsn = self._serialize(command)
        self.client.send(jsn)


    def send_sound_command(self, command: SoundCommand):
        """
        Serialise and send the given SoundCommand to the simulator.
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
            data = self.client.recv(32)

            if data:
                val = data.decode()
                obj_dict = json.loads(val)

                return obj_dict['value']


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
