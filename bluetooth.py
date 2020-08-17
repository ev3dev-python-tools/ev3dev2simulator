import socket

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.connection.client_socket import get_client_socket

RFCOMM = 0


class BluetoothSocket:
    """
    Class mocking the PyBlue BluetoothSocket class to be used for the ev3dev2simulator.
    This is done by wrapping a regular TCP/IP socket into a bluetooth socket interface.
    """

    def __init__(self, comm):
        get_client_socket()  # this is not used for Bluetooth, but to force a connection to the simulator (startup
        # sequence)
        self.port = int(get_simulation_settings()['exec_settings']['bluetooth_port'])
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def accept(self):
        """
        Wrap the created client socket in a ClientWrapper.
        :return: a client wrapper object and its corresponding address.
        """

        client, address = self.server.accept()
        return ClientWrapper(client), address

    def bind(self, tuple):
        """
        Bind and set socket options to REUSEADDR to make sure the socket can be used multiple times
        consecutively without problems.
        :param tuple: which would normally hold the brick's MAC address.
        """

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = self.port + (int(tuple[0].replace(':', ''), 16) % 8192) + tuple[1]
        self.server.bind(('localhost', port))
 
    def close(self):
        self.server.close()

    def connect(self, tuple):
        """
        Connect to localhost instead of the provided address and port.
        :param tuple: which would normally hold the brick's MAC address.
        """
        port = self.port + (int(tuple[0].replace(':', ''), 16) % 8192) + tuple[1]
        self.server.connect(('localhost', port))

    def flush(self):
        pass

    def gettimeout(self):
        return self.server.gettimeout()

    def getsockname(self):
        return self.server.getsockname()

    def listen(self, backlog):
        self.server.listen(backlog)

    def makefile(self, mode="r", buffering=None, encoding=None, errors=None, newline=None):
        return self.server.makefile(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)

    def recv(self, size):
        """
        Receive and decode the data which is in byte form to string, if existent.
        :param size: of data chunk to receive.
        :return: the received data as a string object or None.
        """

        data = self.server.recv(size)

        if data:
            return data.decode()
        else:
            return None

    def send(self, value):
        """
        Send the given value by encoding it to bytes before sending it.
        :param value: to send.
        """

        data = str.encode(value)
        return self.server.send(data)

    def sendall(self, data, flags=None):
        """
        Send the given data. Data needs to be in byte form.
        :param data: to send.
        """

        return self.server.sendall(data)

    def setblocking(self, flag):
        self.server.setblocking(flag)

    def setsockopt(self, level, optname, value):
        pass

    def settimeout(self, value):
        self.server.settimeout(value)


class ClientWrapper:
    """
    Wrapper around a TCP/IP socket client. This wrapper is necessary to encode and decode data before sending.
    This is required because PyBlue allows the sending of strings and TCP/IP sockets only allow bytes.
    """

    def __init__(self, client):
        self.client = client

    def close(self):
        self.client.close()

    def flush(self):
        pass

    def gettimeout(self):
        return self.client.gettimeout()

    def getsockname(self):
        return self.client.getsockname()

    def makefile(self, mode="r", buffering=None, encoding=None, errors=None, newline=None):
        return self.client.makefile(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)

    def recv(self, size):
        """
        Receive and decode the data which is in byte form to string, if existent.
        :param size: of data chunk to receive.
        :return: the received data as a string object or None.
        """

        data = self.client.recv(size)

        if data:
            return data.decode()
        else:
            return None

    def send(self, value):
        """
        Send the given value by encoding it to bytes before sending it.
        :param value: to send.
        """

        data = str.encode(value)
        return self.client.send(data)

    def sendall(self, data, flags=None):
        """
        Send the given data. Data needs to be in byte form.
        :param data: to send.
        """

        return self.client.sendall(data)

    def setblocking(self, flag):
        self.client.setblocking(flag)

    def setsockopt(self, level, optname, value):
        pass

    def settimeout(self, value):
        self.client.settimeout(value)
