class MoveJob:
    __slots__ = [
        'velocity_left',
        'velocity_right',
    ]

    def __init__(self, velocity_left: float, velocity_right: float):
        self.velocity_left = velocity_left
        self.velocity_right = velocity_right
