import json
import socket
import time
from typing import Any, Optional

from ev3dev2simulator.config.config import get_simulation_settings, load_config
from ev3dev2simulator.connection.message.Command import Command


class ClientSocket:
    """
    Class responsible for the establishing and maintaining the socket connection with the simulator.
    This connection is a TCP stream.
    """

    def __init__(self):
        load_config(None)
        port = int(get_simulation_settings()['exec_settings']['socket_port'])

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', port))

        time.sleep(1)

    def send_command(self, command: Command, wait_for_response=False) -> Optional[object]:
        """
        Serialise and send the given Command to the simulator.
        :param command: to send.
        :param wait_for_response: set to True if you expect a result and want to wait for it blocking.
        """

        jsn = self._serialize(command)
        self.client.send(jsn)

        if wait_for_response:
            while True:
                data = self.client.recv(32)

                if data:
                    return self._deserialize(data)

    @staticmethod
    def _serialize(message: Any) -> bytes:
        """
        Serialize the given message so it can be send via a stream channel.
        :param message: to be serialized.
        :return: bytes representing the message.
        """

        obj_dict = message.serialize()

        jsn = json.dumps(obj_dict)
        jsn = jsn.ljust(int(get_simulation_settings()['exec_settings']['message_size']), '#')

        return str.encode(jsn)

    @staticmethod
    def _deserialize(data: bytes) -> Any:
        """
        Deserialize the given data.
        :param data: to be deserialized.
        :return: any type representing value inside the data.
        """

        val = data.decode()
        obj_dict = json.loads(val)

        return obj_dict['value']


client_socket = None


def get_client_socket() -> ClientSocket:
    global client_socket
    if not client_socket:
        client_socket = ClientSocket()
    return client_socket
