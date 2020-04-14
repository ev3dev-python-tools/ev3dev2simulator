import socket
import threading
import time

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.robot.Brick import Brick
from ev3dev2simulator.state import RobotSimulator
from ev3dev2simulator.state.WorldSimulator import WorldSimulator


def create_handler(client, robot_sim: RobotSimulator, brick: Brick) -> ClientSocketHandler:
    """
    Start a ClientSocketHandler tread to manage the given connection.
    :param client: of the connection to manage.
    :param robot_sim: Robot simulator that should be connected
    :param brick: Brick that is going to execute the commands
    :return: a newly created ClientSocketHandler object.
    """
    handler = ClientSocketHandler(robot_sim, client, brick.brick, brick.name)
    handler.setDaemon(True)
    handler.start()

    return handler


def is_any_handler_disconnected(handlers):
    for handler in handlers:
        if not handler.is_running:
            return True
    return False


class ServerSockets(threading.Thread):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """

    def __init__(self, world_simulator: WorldSimulator):
        threading.Thread.__init__(self)
        self.word_simulator = world_simulator

    def run(self):
        """
        Listen for incoming connections. When a connection is established spawn a ClientSocketHandler
        to manage it. Two connections can be established at the same time.
        When one connection is closed close the other one as well and start listening
        for two new connections.
        """

        port = get_simulation_settings()['exec_settings']['socket_port']

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)

        print('Listening for connections...')
        while True:
            self.handle_sockets(server)

    def handle_sockets(self, server):
        while True:
            handlers = []
            server.setblocking(False)
            server.settimeout(1)
            for robot_sim in self.word_simulator.robot_simulators:
                for brick in robot_sim.robot.get_bricks():
                    print(f'Please connect brick "{brick.name}" from robot "{robot_sim.robot.name}" ')
                    while True:
                        try:
                            (client, address) = server.accept()
                            handlers.append(create_handler(client, robot_sim, brick))
                        except socket.timeout:
                            if self.handle_disconnected_clients(handlers):
                                return
                            continue
                        break

            time.sleep(1)
            print('All bricks connected, disconnect one to reset the playing field')
            while True:
                if self.handle_disconnected_clients(handlers):
                    break
                else:
                    time.sleep(1)


    def handle_disconnected_clients(self, handlers):
        if is_any_handler_disconnected(handlers):
            for handler in handlers:
                handler.is_running = False
            time.sleep(1)  # give some time to prevent handler from requesting data
            self.word_simulator.request_reset()
            print('All connections closed')
            return True
        return False

