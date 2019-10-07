class SoundCommand:
    """
    Command send from the ev3dev2 mock to the simulator telling the robot to display the supplied message.
    """


    def __init__(self, message: str):
        self.message = message


    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """

        return {
            'type': 'SoundCommand',
            'message': self.message
        }
