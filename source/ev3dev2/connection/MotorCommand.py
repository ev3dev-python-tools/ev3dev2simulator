class MotorCommand:

    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int,
                 frames_coast: int):
        self.address = address
        self.ppf = ppf
        self.frames = frames
        self.frames_coast = frames_coast


    def serialize(self) -> dict:
        return {
            'type': 'MotorCommand',
            'address': self.address,
            'ppf': self.ppf,
            'frames': self.frames,
            'frames_coast': self.frames_coast
        }
