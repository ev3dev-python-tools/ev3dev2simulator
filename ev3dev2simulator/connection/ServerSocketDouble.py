import socket
import threading
import time

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ClientSocketHandler import ClientSocketHandler
from ev3dev2simulator.state import RobotState


class ServerSocketDouble(threading.Thread):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """


    def __init__(self, robot_state: RobotState, first_side: str):
        threading.Thread.__init__(self)
        self.robot_state = robot_state
        self.first_run = True

        self.client1_name = 'left_brick' if first_side == 'left' else 'right_brick'
        self.client2_name = 'right_brick' if first_side == 'left' else 'left_brick'


    def run(self):
        """
        Listen for incoming connections. When a connection is established spawn a ClientSocketHandler
        to manage it. Two connections can be established at the same time.
        When one connection is closed close the other one as well and start listening
        for two new connections.
        """

        port = get_config().get_data()['exec_settings']['socket_port']

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)

        while True:
            print('Listening for connections...')

            (client1, address1) = server.accept()
            handler1 = self.create_handler(client1, self.client1_name)

            (client2, address2) = server.accept()
            handler2 = self.create_handler(client2, self.client2_name)

            if not self.first_run:
                self.robot_state.should_reset = True

            self.first_run = False
            time.sleep(1)

            while True:

                if not handler1.is_running:
                    handler2.is_running = False
                    break

                elif not handler2.is_running:
                    handler1.is_running = False
                    break

                else:
                    time.sleep(1)

            time.sleep(1)
            print('All connections closed')


    def create_handler(self, client, connection_id: str) -> ClientSocketHandler:
        """
        Start a ClientSocketHandler tread to manage the given connection.
        :param client: of the connection to manage.
        :param connection_id: of the connection.
        :return: a newly created ClientSocketHandler object.
        """

        handler = ClientSocketHandler(self.robot_state, client, connection_id)
        handler.setDaemon(True)
        handler.start()

        return handler
