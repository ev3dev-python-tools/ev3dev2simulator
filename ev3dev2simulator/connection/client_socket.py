"""
Singleton module client_sockets contains the class ClientSocket and the function get_client_socket to get the instance.
"""

import json
import socket
import threading
import time
import sys
from typing import Any, Optional
from ev3dev2simulator.config.config import get_simulation_settings, load_config
from ev3dev2simulator.connection.message.command import Command

THIS = sys.modules[__name__]


class ClientSocket:
    """
    Class responsible for the establishing and maintaining the socket connection with the simulator.
    This connection is a TCP stream.
    """

    def __init__(self):
        load_config(None)
        port = int(get_simulation_settings()['exec_settings']['socket_port'])

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.settimeout(0.1)

        self.client.connect(('localhost', port))
        self.lock = threading.Lock()

        time.sleep(1)

    def send_command(self, command: Command, wait_for_response=False) -> Optional[object]:
        """
        Serialise and send the given Command to the simulator.
        :param command: to send.
        :param wait_for_response: set to True if you expect a result and want to wait for it blocking.
        """
        self.lock.acquire()
        jsn = self.serialize(command)

        des = None
        try:
            self.client.send(jsn)
            if wait_for_response:
                data = self.client.recv(32)
                des = self.deserialize(data)
        finally:
            self.lock.release()
        return des

    @staticmethod
    def serialize(message: Any) -> bytes:
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
    def deserialize(data: bytes) -> Any:
        """
        Deserialize the given data.
        :param data: to be deserialized.
        :return: any type representing value inside the data.
        """

        val = data.decode()
        obj_dict = json.loads(val)

        return obj_dict['value']


THIS.CLIENT_SOCKET = None


def get_client_socket() -> ClientSocket:
    """
    Functionality to make clientSocket a singleton. Creates a client if it does not exists and returns it either way.
    """
    if not THIS.CLIENT_SOCKET:
        THIS.CLIENT_SOCKET = ClientSocket()
    return THIS.CLIENT_SOCKET
