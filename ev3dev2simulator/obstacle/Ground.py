from arcade import create_rectangle
from ev3dev2simulator.util.Util import apply_scaling


class Ground:
    def __init__(self, x, y, width, height, color):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

        # visualisation
        self.color = color
        self.shape = None

    def get_shapes(self):
        if self.shape is None:
            self.create_shape()
        return [self.shape]

    def create_shape(self):
        self.shape = create_rectangle(apply_scaling(self.center_x),
                                      apply_scaling(self.center_y), apply_scaling(self.width),
                                      apply_scaling(self.height),
                                      self.color)
