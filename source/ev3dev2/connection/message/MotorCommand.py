class MotorCommand:

    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int):
        self.address = address
        self.ppf = ppf
        self.frames = frames


    def serialize(self) -> dict:
        return {}
