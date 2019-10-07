import json
import socket
import threading
import time
from typing import Any

from ev3dev2.simulator.config.config import load_config
from ev3dev2.simulator.connection.MessageProcessor import MessageProcessor
from ev3dev2.simulator.connection.message.DataRequest import DataRequest
from ev3dev2.simulator.connection.message.DriveCommand import DriveCommand
from ev3dev2.simulator.connection.message.SoundCommand import SoundCommand
from ev3dev2.simulator.connection.message.StopCommand import StopCommand


class ServerSocket(threading.Thread):
    """
    Class responsible for listening to incoming socket connections from ev3dev2 mock processes.
    """


    def __init__(self, robot_state):
        threading.Thread.__init__(self)
        self.message_processor = MessageProcessor(robot_state)
        self.robot_state = robot_state


    def run(self):
        """
        Listen for incoming connections. Start listening for messages when a connection is established.
        When the connection breaks up listen for a new connection.
        """

        port = load_config()['exec_settings']['socket_port']

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', port))
        server.listen(5)

        while True:
            print('Listening for connections...')
            (client, address) = server.accept()

            print('Connection accepted')
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

            self.robot_state.should_reset = True


    def _process(self, data: bytes) -> bytes:
        """
        Process incoming data by decoding it and sending it to the MessageProcessor.
        :param data: to process.
        :return: a possible response in bytes when the incoming message requires it.
        """

        jsn = data.decode()
        jsn = jsn.replace('#', '')

        obj_dict = json.loads(jsn)

        tpe = obj_dict['type']
        if tpe == 'DriveCommand':
            return self._process_drive_command(obj_dict)

        if tpe == 'StopCommand':
            return self._process_stop_command(obj_dict)

        if tpe == 'SoundCommand':
            return self._process_sound_command(obj_dict)

        elif tpe == 'DataRequest':
            return self._process_data_request(obj_dict)


    def _process_drive_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a DriveCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = DriveCommand(d['address'], d['ppf'], d['frames'], d['frames_coast'])
        self.message_processor.process_drive_command(command)

        return None


    def _process_stop_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a StopCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = StopCommand(d['address'], d['ppf'], d['frames'])
        self.message_processor.process_stop_command(command)

        return None


    def _process_sound_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a SoundCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = SoundCommand(d['message'])
        self.message_processor.process_sound_command(command)

        return None


    def _process_data_request(self, d: dict) -> bytes:
        """
        Deserialize the given dictionary into a DataRequest and send it to the MessageProcessor.
        Return a serialized response with the requested value.
        :param d: to process.
        :return: a bytes object representing the serialized response.
        """

        request = DataRequest(d['address'])
        value = self.message_processor.process_data_request(request)

        return self._serialize_response(value)


    def _serialize_response(self, value) -> bytes:
        """
        Serialize the given value into a bytes object containing a dictionary.
        :param value: to serialize.
        """

        d = {'value': value}

        jsn = json.dumps(d)
        return str.encode(jsn)
