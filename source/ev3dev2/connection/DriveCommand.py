from ev3dev2.connection.MotorCommand import MotorCommand


class DriveCommand(MotorCommand):

    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int,
                 frames_coast: int):
        super().__init__(address, ppf, frames)
        self.frames_coast = frames_coast


    def serialize(self) -> dict:
        return {
            'type': 'DriveCommand',
            'address': self.address,
            'ppf': self.ppf,
            'frames': self.frames,
            'frames_coast': self.frames_coast
        }
