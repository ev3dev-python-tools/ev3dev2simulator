from arcade import create_rectangle


class Ground:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height

        # visualisation
        self.color = color
        self.shape = None

    def get_shapes(self):
        return [self.shape]

    def create_shape(self, x, y, width, height):
        self.shape = create_rectangle(x, y, width, height, self.color)
