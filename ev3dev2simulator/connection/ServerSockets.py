import socket
import threading
import time

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.state.WorldSimulator import WorldSimulator


class ServerSockets(threading.Thread):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """

    def __init__(self, world_simulator: WorldSimulator):
        threading.Thread.__init__(self)
        self.word_simulator = world_simulator
        self.brick_sockets = {}
        self.first_connected = False

    def run(self):
        """
        Listen for incoming connections. When a connection is established spawn a ClientSocketHandler
        to manage it. Multiple connections can be established at the same time.
        """

        port = get_simulation_settings()['exec_settings']['socket_port']

        for robot_sim in self.word_simulator.robot_simulators:
            for brick in robot_sim.robot.get_bricks():
                sock = ClientSocketHandler(robot_sim, brick.brick, brick.name)
                sock.setDaemon(True)
                sock.start()
                self.brick_sockets[(robot_sim.robot.name, brick.name)] = sock

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)
        server.setblocking(False)
        server.settimeout(1)

        print('Listening for connections...')
        self.handle_sockets(server)
        print('Closing server')

    def handle_sockets(self, server):
        show_message = True
        while True:
            for (robot_name, brick_name), sock in self.brick_sockets.items():
                if not sock.is_connected:
                    if show_message:
                        print(f'Please connect brick "{brick_name}" from robot "{robot_name}" ')
                        show_message = False
                    try:
                        (client, address) = server.accept()
                        self.first_connected = True
                        print(
                            f'Connection from \"{brick_name}\" from robot \"{robot_name}\" '
                            'accepted\n')
                        sock.client = client
                        sock.is_connected = True
                        show_message = True
                        break
                    except socket.timeout:
                        pass
            if self.all_sockets_are_disconnected(self.brick_sockets.values()) and self.first_connected:
                self.word_simulator.request_reset()
            time.sleep(1)

    @staticmethod
    def all_sockets_are_disconnected(sockets):
        """
        Check if all sockets are disconnected.
        :param sockets: the sockets to check for their connection
        :return: boolean indicating that all sockets are disconnected
        """
        return all(map(lambda brick_socket: not brick_socket.is_connected, sockets))


