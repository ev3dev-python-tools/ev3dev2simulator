import socket
import threading
import time

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.robot.Brick import Brick
from ev3dev2simulator.state import RobotSimulator


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


class ServerSockets(threading.Thread):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """

    def __init__(self, robot_simulators: [RobotSimulator]):
        threading.Thread.__init__(self)
        self.robot_simulators = robot_simulators
        self.first_run = True

    def run(self):
        """
        Listen for incoming connections. When a connection is established spawn a ClientSocketHandler
        to manage it. Two connections can be established at the same time.
        When one connection is closed close the other one as well and start listening
        for two new connections.
        """

        port = get_config().get_visualisation_config()['exec_settings']['socket_port']

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)

        while True:
            print('Listening for connections...')

            handlers = []

            for robot_sim in self.robot_simulators:
                for brick in robot_sim.robot.get_bricks():
                    print(f'Please connect brick "{brick.name}" from robot "{robot_sim.robot.name}" ')
                    (client, address) = server.accept()
                    handlers.append(create_handler(client, robot_sim, brick))

            if not self.first_run:
                for robot_sim in self.robot_simulators:
                    robot_sim.should_reset = True

            self.first_run = False
            time.sleep(1)

            while True:
                if is_any_handler_disconnected(handlers):
                    time.sleep(1)
                    print('All connections closed')
                    break
                else:
                    time.sleep(1)

