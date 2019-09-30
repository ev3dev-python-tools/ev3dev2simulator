from ev3dev2.connection.message.MotorCommand import MotorCommand


class DriveCommand(MotorCommand):
    """
    Command send from the ev3dev2 mock to the simulator telling the motor with the supplied address to rotate (drive).
    This is done at the given speed in pixels per second for the given number of frames.
    This command also includes how many frames it has to come to a halt.
    If coast_frames is a positive non-zero number the motor is instructed to coast to a halt when the driving is completed.
    """


    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int,
                 frames_coast: int):
        super(DriveCommand, self).__init__(address, ppf, frames)
        self.frames_coast = frames_coast


    def serialize(self) -> dict:
        return {
            'type': 'DriveCommand',
            'address': self.address,
            'ppf': self.ppf,
            'frames': self.frames,
            'frames_coast': self.frames_coast
        }
