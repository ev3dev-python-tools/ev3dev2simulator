import socket
import sys
import threading
import unittest

from ev3dev2simulator.config.config import get_simulation_settings, load_config
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand


class TestClientSocket(unittest.TestCase):

    def setUp(self) -> None:
        load_config(None)

    def run_fake_server(self):
        # Run a server to listen for a connection and then close it
        port = get_simulation_settings()['exec_settings']['socket_port']
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('localhost', port))
        server_sock.listen(5)
        (client, address) = server_sock.accept()
        while True:
            data = client.recv(128)
            if data:
                if data == b'close_test_server':
                    client.close()
                    server_sock.close()
                    return

    def test_serialize_deserialize(self):
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()
        from ev3dev2simulator.connection.ClientSocket import get_client_socket
        sock = get_client_socket()

        command = RotateCommand('test_port', 500.0, 100.0, 'hold')
        sock.send_command(command)

        ser = sock._serialize(command)
        self.assertEqual(ser, b'{"type": "RotateCommand", "address": "test_port", "speed": 500.0, "distance"'
                              b': 100.0, "stop_action": "hold"}#####################')

        ser = b'{"value": 15}'
        deser = sock._deserialize(ser)
        self.assertEqual(deser, 15)

        sock.client.send(str.encode('close_test_server'))
        sock.client.close()
        server_thread.join()



if __name__ == '__main__':
    unittest.main()
