import json
import socket
import time
from typing import Any

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.message import MotorCommand, SoundCommand, DataRequest, LedCommand


class ClientSocket:
    """
    Class responsible for the establishing and maintaining the socket connection with the simulator.
    This connection is a TCP stream.
    """


    def __init__(self):
        port = get_config().get_data()['exec_settings']['socket_port']

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', port))

        time.sleep(1)


    def send_motor_command(self, command: MotorCommand) -> float:
        """
        Serialise and send the given MotorCommand to the simulator.
        :param command: to send.
        """

        jsn = self._serialize(command)
        self.client.send(jsn)

        return self._wait_for_response()


    def send_led_command(self, command: LedCommand):
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

        return self._wait_for_response()


    def _wait_for_response(self) -> Any:
        """
        Wait until the simulator responds with a message and deserialize the message.
        This function blocks until a response has been received.
        :return: the value of the responded message.
        """

        while True:
            data = self.client.recv(32)

            if data:
                return self._deserialize(data)


    def _serialize(self, message: Any) -> bytes:
        """
        Serialize the given message so it can be send via a stream channel.
        :param message: to be serialized.
        :return: bytes representing the message.
        """

        obj_dict = message.serialize()

        jsn = json.dumps(obj_dict)
        jsn = jsn.ljust(128, '#')

        return str.encode(jsn)


    def _deserialize(self, data: bytes) -> Any:
        """
        Deserialize the given data.
        :param data: to be deserialized.
        :return: any type representing value inside the data.
        """

        val = data.decode()
        obj_dict = json.loads(val)

        return obj_dict['value']


client_socket = ClientSocket()


def get_client_socket() -> ClientSocket:
    return client_socket
