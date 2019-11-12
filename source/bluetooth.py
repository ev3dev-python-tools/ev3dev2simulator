import socket

from ev3dev2.simulator.config.config import load_config

RFCOMM = 0


class BluetoothSocket:

    def __init__(self, comm):
        self.port = load_config()['exec_settings']['bluetooth_port']
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def accept(self):
        return self.server.accept()


    def bind(self, tuple):
        self.server.bind(('localhost', self.port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def close(self):
        self.server.close()


    def connect(self, tuple):
        self.server.connect(('localhost', self.port))


    def flush(self):
        pass


    def gettimeout(self):
        return self.server.gettimeout()


    def getsockname(self):
        return self.server.getsockname()


    def listen(self, backlog):
        self.server.listen(backlog)


    def makefile(self, mode="r", buffering=None, *, encoding=None, errors=None, newline=None):
        return self.server.makefile(mode, buffering, encoding, errors, newline)


    def recv(self, size):
        return self.server.recv(size)


    def send(self, data):
        return self.server.send(data)


    def setblocking(self, flag):
        self.server.setblocking(flag)


    def setsockopt(self, level, optname, value):
        pass


    def settimeout(self, value):
        self.server.settimeout(value)
