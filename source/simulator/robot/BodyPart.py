import arcade


class BodyPart(arcade.Sprite):

    def __init__(self, src: str, scale: float):
        super().__init__(src, scale)


    def move_x(self, x: float):
        self.center_x += x


    def move_y(self, y: float):
        self.center_y += y
