import json
import socket
import threading
from typing import Any

from ev3dev2.simulator.connection.MessageProcessor import MessageProcessor
from ev3dev2.simulator.connection.message.DataRequest import DataRequest
from ev3dev2.simulator.connection.message.LedCommand import LedCommand
from ev3dev2.simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2.simulator.connection.message.SoundCommand import SoundCommand
from ev3dev2.simulator.connection.message.StopCommand import StopCommand


class ClientSocketHandler(threading.Thread):
    """
    Class responsible for managing a socket connection from the ev3dev2 mock processes.
    """


    def __init__(self, robot_state, client, connection_id):
        threading.Thread.__init__(self)

        self.message_processor = MessageProcessor(robot_state)
        self.robot_state = robot_state
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
        if tpe == 'RotateCommand':
            return self._process_drive_command(obj_dict)

        if tpe == 'StopCommand':
            return self._process_stop_command(obj_dict)

        if tpe == 'SoundCommand':
            return self._process_sound_command(obj_dict)

        if tpe == 'LedCommand':
            return self._process_led_command(obj_dict)

        elif tpe == 'DataRequest':
            return self._process_data_request(obj_dict)


    def _process_drive_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a RotateCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = RotateCommand(d['address'], d['speed'], d['distance'], d['stop_action'])
        value = self.message_processor.process_rotate_command(command)

        return self._serialize_response(value)


    def _process_stop_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a StopCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = StopCommand(d['address'], d['speed'], d['stop_action'])
        value = self.message_processor.process_stop_command(command)

        return self._serialize_response(value)


    def _process_led_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a LedCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        # print(d['address'] + '  --  ' + str(d['brightness']))
        command = LedCommand(d['address'], d['brightness'])
        self.message_processor.process_led_command(command)

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
