import socket

from ev3dev2simulator.connection.MessageHandler import MessageHandler
from ev3dev2simulator.connection.MessageProcessor import MessageProcessor
from ev3dev2simulator.state import RobotState


class ClientSocketHandler(MessageHandler):
    """
    Class responsible for managing a socket connection from the ev3dev2 mock processes.
    """


    def __init__(self, robot_state: RobotState, client, connection_id: str):
        super(ClientSocketHandler, self).__init__(MessageProcessor(connection_id, robot_state))

        self.client = client
        self.connection_id = connection_id
        self.is_running = True


    def run(self):
        """
        Manage the socket connection.
        """

        print('Connection ' + self.connection_id + ' accepted')

        try:
            while self.is_running:

                data = self.client.recv(128)
                if data:

                    val = self._process(data)
                    if val:
                        self.client.send(val)

                else:
                    self.is_running = False

        except socket.error:
            self.is_running = False

        print('Closing connection ' + self.connection_id + '...')
        self.client.close()
