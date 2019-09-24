from ev3dev2.connection.message.MotorCommand import MotorCommand


class StopCommand(MotorCommand):

    def __init__(self,
                 address: str,
                 ppf: float,
                 frames: int):
        super(StopCommand, self).__init__(address, ppf, frames)


    def serialize(self) -> dict:
        return {
            'type': 'StopCommand',
            'address': self.address,
            'ppf': self.ppf,
            'frames': self.frames
        }
