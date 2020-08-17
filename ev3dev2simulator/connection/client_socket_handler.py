"""
The client_socket_handler is used to communicate with a client opened by robot code.
"""

import socket
import threading
from time import sleep

from ev3dev2simulator.config.config import get_simulation_settings
from ev3dev2simulator.connection.message_handler import MessageHandler
from ev3dev2simulator.state.message_processor import MessageProcessor
from ev3dev2simulator.state import robot_simulator


class ClientSocketHandler(threading.Thread):
    """
    Class responsible for managing a socket connection from the ev3dev2 mock processes.
    """

    def __init__(self, robot_sim: robot_simulator, brick_id: int, brick_name: str):
        threading.Thread.__init__(self)
        self.message_handler = MessageHandler(MessageProcessor(brick_id, robot_sim))
        self.client = None
        self.brick_id = brick_id
        self.is_running = True
        self.is_connected = False
        self.brick_name = brick_name
        self.robot_sim = robot_sim
        self.message_size = int(get_simulation_settings()['exec_settings']['message_size'])

    def run(self):
        """
        Manage the socket connection.
        """
        while self.is_running:
            if not self.is_connected:
                sleep(0.1)
            else:
                try:
                    data = self.client.recv(self.message_size)
                    if data:
                        val = self.message_handler.process(data)
                        if val:
                            self.client.send(val)
                    else:
                        self.is_connected = False
                except socket.error:
                    self.is_connected = False
                    self.robot_sim.reset_queues_of_brick(self.brick_id)
                    print(f'Closing connection from \"{self.brick_name}\" (id: {self.brick_id}) from robot '
                          f'\"{self.robot_sim.robot.name}\"')
                    self.client.close()
