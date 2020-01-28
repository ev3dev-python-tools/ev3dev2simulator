import json
import threading
from typing import Any

from ev3dev2simulator.connection import MessageProcessor
from ev3dev2simulator.connection.message.DataRequest import DataRequest
from ev3dev2simulator.connection.message.LedCommand import LedCommand
from ev3dev2simulator.connection.message.RotateCommand import RotateCommand
from ev3dev2simulator.connection.message.SoundCommand import SoundCommand
from ev3dev2simulator.connection.message.StopCommand import StopCommand


class MessageHandler(threading.Thread):

    def __init__(self, message_processor: MessageProcessor):
        threading.Thread.__init__(self)

        self.message_processor = message_processor


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
