from arcade import create_rectangle


class Ground:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # visualisation
        self.color = color
        self.shape = None

    def get_shapes(self):
        if self.shape is None:
            self.create_shape()
        return [self.shape]

    def create_shape(self, scale):
        self.shape = create_rectangle(self.x * scale, self.y * scale, self.width * scale,
                                      self.height * scale, self.color)
