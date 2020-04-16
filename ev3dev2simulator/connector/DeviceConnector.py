import ev3dev2
from ev3dev2simulator.connection.ClientSocket import get_client_socket
from ev3dev2simulator.connection.message.ConfigRequest import ConfigRequest


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

    def request_device_config(self, kwargs):
        """
        Requests the port that the device is attached to. This helps preventing errors if a port is given,
        or retrieves the port that should be used.
        """
        request = ConfigRequest(kwargs)
        new_port = self.client_socket.send_command(request, True)
        if new_port == 'dev_not_connected':
            raise ev3dev2.DeviceNotFound(
                f'Could not find device of type(s) {kwargs.get("driver_name")} {f"on port {self.address}" if self.address else ""}')
        return new_port
