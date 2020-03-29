import socket
import threading

from ev3dev2simulator.connection.MessageHandler import MessageHandler
from ev3dev2simulator.state.MessageProcessor import MessageProcessor
from ev3dev2simulator.state import RobotSimulator


class ClientSocketHandler(threading.Thread):
    """
    Class responsible for managing a socket connection from the ev3dev2 mock processes.
    """

    def __init__(self, robot_sim: RobotSimulator, client, brick_id: int, brick_name: str):
        threading.Thread.__init__(self)
        self.message_handler = MessageHandler(MessageProcessor(brick_id, robot_sim))
        self.client = client
        self.brick_id = brick_id
        self.is_running = True
        self.brick_name = brick_name
        self.robot_sim = robot_sim

    def run(self):
        """
        Manage the socket connection.
        """

        print(f'Connection from \"{self.brick_name}\" (id: {self.brick_id}) from robot \"{self.robot_sim.robot.name}\" '
              'accepted\n')

        try:
            while self.is_running:

                data = self.client.recv(128)
                if data:

                    val = self.message_handler.process(data)
                    if val:
                        self.client.send(val)

                else:
                    self.is_running = False

        except socket.error:
            self.is_running = False
        print(f'Closing connection from \"{self.brick_name}\" (id: {self.brick_id}) from robot '
              f'\"{self.robot_sim.robot.name}\"')
        self.client.close()
