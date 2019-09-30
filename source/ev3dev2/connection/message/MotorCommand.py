class MotorCommand:
    """
    Base class for a motor command sent from the ev3dev2 mock to the simulator.
    """


    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int):
        self.address = address
        self.ppf = ppf
        self.frames = frames


    def serialize(self) -> dict:
        """
        Serialize the data of this command into a dictionary.
        """

        return {}
