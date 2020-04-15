from ev3dev2simulator.connection.ClientSocket import get_client_socket
from ev3dev2simulator.connection.message.DataRequest import DataRequest


class DeviceConnector:
    """
    The DeviceConnector class provides a translation layer between the ev3dev2 device classes
    and the devices on the simulated robot.
    This class is responsible for determining the correct configuration of the device.
    """

    def __init__(self, address, class_name):
        self.address = address
        self.class_name = class_name
        self.client_socket = get_client_socket()

    def request_device_config(self):
        """
        Requests the port that the device is attached to. This helps preventing errors if a port is given,
        or retrieves the port that should be used.
        """
        request = DataRequest(self.address, self.class_name)
        return self.client_socket.send_command(request, True)
