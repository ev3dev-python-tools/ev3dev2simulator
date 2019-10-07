from ev3dev2.simulator.connection.message.MotorCommand import MotorCommand


class StopCommand(MotorCommand):
    """
    Command send from the ev3dev2 mock to the simulator telling the motor with the supplied address to stop.
    This command also includes the current speed of the motor and how many frames it has to come to a halt.
    If frames is a positive non-zero number the motor is instructed to coast to a halt.
    """


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
