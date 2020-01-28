class LedCommand:
    """
    Command send from the ev3dev2 mock to the simulator telling the robot to display the supplied message.
    """


    def __init__(self, address: str, brightness: float):
        self.address = address
        self.brightness = brightness


    def get_led_id(self):
        return self.address.split(':')[0]


    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """

        return {
            'type': 'LedCommand',
            'address': self.address,
            'brightness': self.brightness
        }
