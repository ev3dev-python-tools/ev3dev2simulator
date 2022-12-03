"""
The message_handler module contains the MessageHandler class.
"""

import json
from logging import warning
from typing import Any

from ev3dev2simulator.connection.message.config_request import ConfigRequest
from ev3dev2simulator.state.message_processor import MessageProcessor
from ev3dev2simulator.connection.message.data_request import DataRequest
from ev3dev2simulator.connection.message.led_command import LedCommand
from ev3dev2simulator.connection.message.rotate_command import RotateCommand
from ev3dev2simulator.connection.message.sound_command import SoundCommand
from ev3dev2simulator.connection.message.stop_command import StopCommand


class MessageHandler:
    """
    The MessageHandler class processes message from bytes to an object understood by the simulator.
    """
    def __init__(self, message_processor: MessageProcessor):
        self.message_processor = message_processor

    def process(self, data: bytes) -> bytes:
        """
        Process incoming data by decoding it and sending it to the MessageProcessor.
        :param data: to process.
        :return: a possible response in bytes when the incoming message requires it.
        """

        jsn = data.decode()
        jsn = jsn.replace('#', '')

        obj_dict = json.loads(jsn)

        tpe = obj_dict['type']

        # handling any Command requests
        if tpe == 'RotateCommand':
            return self._process_drive_command(obj_dict)

        if tpe == 'StopCommand':
            return self._process_stop_command(obj_dict)

        if tpe == 'SoundCommand':
            return self._process_sound_command(obj_dict)

        if tpe == 'LedCommand':
            return self._process_led_command(obj_dict)


        # handling any data or config requests.
        if tpe == 'DataRequest':
            return self._process_data_request(obj_dict)
        if tpe == 'ConfigRequest':
            return self._process_config_request(obj_dict)

        warning(f'Unknown command type {tpe}')
        return bytes()

    def _process_drive_command(self, command_dict: dict) -> Any:
        """
        Deserialize the given dictionary into a RotateCommand and send it to the MessageProcessor.
        :param command_dict: to process.
        """
        command = RotateCommand(command_dict['address'], command_dict['speed'],
                                command_dict['distance'], command_dict['stop_action'])
        value = self.message_processor.process_rotate_command(command)

        return self.serialize_response(value)

    def _process_stop_command(self, command_dict: dict) -> Any:
        """
        Deserialize the given dictionary into a StopCommand and send it to the MessageProcessor.
        :param command_dict: to process.
        """

        command = StopCommand(command_dict['address'], command_dict['speed'], command_dict['stop_action'])
        value = self.message_processor.process_stop_command(command)

        return self.serialize_response(value)

    def _process_led_command(self, command_dict: dict) -> Any:
        """
        Deserialize the given dictionary into a LedCommand and send it to the MessageProcessor.
        :param command_dict: to process.
        """

        command = LedCommand(command_dict['address'], command_dict['brightness'])
        self.message_processor.process_led_command(command)

    def _process_sound_command(self, command_dict: dict) -> Any:
        """
        Deserialize the given dictionary into a SoundCommand and send it to the MessageProcessor.
        :param command_dict: to process.
        """

        command = SoundCommand(command_dict['message'], command_dict['duration'], command_dict['soundType'])
        self.message_processor.process_sound_command(command)

    def _process_data_request(self, command_dict: dict) -> bytes:
        """
        Deserialize the given dictionary into a DataRequest and send it to the MessageProcessor.
        Return a serialized response with the requested value.
        :param command_dict: to process.
        :return: a bytes object representing the serialized response.
        """
        request = DataRequest(command_dict['address'])
        value = self.message_processor.process_data_request(request)

        return self.serialize_response(value)

    def _process_config_request(self, command_dict: dict):
        """
        Deserialize the given dictionary into a ConfigRequest and send it to the MessageProcessor.
        Return a serialized response with the determined port or a 'dev_not_connected' string.
        :param d: to process.
        :return: a bytes object representing the serialized response.
        """
        request = ConfigRequest(command_dict['kwargs'], command_dict['class_name'])
        value = self.message_processor.process_config_request(request)

        return self.serialize_response(value)


    @staticmethod
    def serialize_response(value) -> bytes:
        """
        Serialize the given value into a bytes object containing a dictionary.
        :param value: to serialize.
        """

        command_dict = {'value': value}

        jsn = json.dumps(command_dict)
        return str.encode(jsn)
