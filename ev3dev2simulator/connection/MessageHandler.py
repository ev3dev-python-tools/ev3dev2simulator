import json
from logging import warning
from typing import Any

from ev3dev2simulator.connection.message.ConfigRequest import ConfigRequest
from ev3dev2simulator.state import message_processor
from ev3dev2simulator.connection.message.DataRequest import DataRequest
from ev3dev2simulator.connection.message.LedCommand import LedCommand
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand
from ev3dev2simulator.connection.message.StopCommand import StopCommand


class MessageHandler:

    def __init__(self, message_processor: message_processor):
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
        if tpe == 'RotateCommand':
            return self._process_drive_command(obj_dict)

        elif tpe == 'StopCommand':
            return self._process_stop_command(obj_dict)

        elif tpe == 'SoundCommand':
            return self._process_sound_command(obj_dict)

        elif tpe == 'LedCommand':
            return self._process_led_command(obj_dict)

        elif tpe == 'DataRequest':
            return self._process_data_request(obj_dict)

        elif tpe == 'ConfigRequest':
            return self._process_config_request(obj_dict)
        else:
            warning(f'Unknown command type {tpe}')


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

        command = LedCommand(d['address'], d['brightness'])
        self.message_processor.process_led_command(command)

        return None

    def _process_sound_command(self, d: dict) -> Any:
        """
        Deserialize the given dictionary into a SoundCommand and send it to the MessageProcessor.
        :param d: to process.
        """

        command = SoundCommand(d['message'], d['duration'], d['soundType'])
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

    def _process_config_request(self, d: dict):
        """
        Deserialize the given dictionary into a ConfigRequest and send it to the MessageProcessor.
        Return a serialized response with the determined port or a 'dev_not_connected' string.
        :param d: to process.
        :return: a bytes object representing the serialized response.
        """
        request = ConfigRequest(d['kwargs'], d['class_name'])
        value = self.message_processor.process_config_request(request)

        return self._serialize_response(value)


    @staticmethod
    def _serialize_response(value) -> bytes:
        """
        Serialize the given value into a bytes object containing a dictionary.
        :param value: to serialize.
        """

        d = {'value': value}

        jsn = json.dumps(d)
        return str.encode(jsn)
