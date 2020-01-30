import socket
import time

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.MessageHandler import MessageHandler
from ev3dev2simulator.connection.MessageProcessor import MessageProcessor
from ev3dev2simulator.state import RobotState


class ServerSocketSingle(MessageHandler):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """


    def __init__(self, robot_state: RobotState):
        super(ServerSocketSingle, self).__init__(MessageProcessor('', robot_state))

        self.robot_state = robot_state
        self.first_run = True


    def run(self):
        """
        Listen for incoming connections. Start listening for messages when a connection is established.
        When the connection breaks up listen for a new connection.
        """

        port = get_config().get_data()['exec_settings']['socket_port']

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)

        while True:
            print('Listening for connections...')
            (client, address) = server.accept()

            print('Connection accepted')
            if not self.first_run:
                self.robot_state.should_reset = True

            self.first_run = False
            time.sleep(1)

            try:
                while True:
                    data = client.recv(128)
                    if data:
                        val = self._process(data)
                        if val:
                            client.send(val)

                    else:
                        break

            except socket.error:
                pass

            print('Closing connection...')
            client.close()
