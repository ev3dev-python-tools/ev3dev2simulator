from arcade import Sprite

from source.simulator.robot.Body import Body
from source.simulator.robot.ColorSensor import ColorSensor
from source.simulator.robot.TouchSensor import TouchSensor
from source.simulator.robot.Wheel import Wheel


class Robot:
    def __init__(self, img_cfg, center_x: int, center_y: int):

        self.body = Body(img_cfg, center_x, center_y)
        self.left_wheel = Wheel(img_cfg, self.body, 45, 25)
        self.right_wheel = Wheel(img_cfg, self.body, -45, 25)

        self.left_color_sensor = ColorSensor(img_cfg, self.body, 45, 70)
        self.center_color_sensor = ColorSensor(img_cfg, self.body, 0, 65)
        self.right_color_sensor = ColorSensor(img_cfg, self.body, -45, 70)

        self.left_touch_sensor = TouchSensor(img_cfg, self.body, 50, 85, True)
        self.right_touch_sensor = TouchSensor(img_cfg, self.body, -50, 85, False)

        self.sprites = [self.body,
                        self.left_wheel,
                        self.right_wheel,
                        self.left_color_sensor,
                        self.center_color_sensor,
                        self.right_color_sensor,
                        self.left_touch_sensor,
                        self.right_touch_sensor]

    def move_x(self, x: int):
        for s in self.get_sprites():
            s.move_x(x)

    def move_y(self, y: int):
        for s in self.get_sprites():
            s.move_y(y)

    def rotate(self, degrees: int):
        for s in self.get_sprites():
            s.rotate(degrees)

    def get_sprites(self) -> [Sprite]:
        return self.sprites
