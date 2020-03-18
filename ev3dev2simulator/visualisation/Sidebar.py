import sys
import arcade


class Sidebar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.show_sensor_connection = True

        self.text_size = 10
        self.text_spacing = 10
        self.left_text_padding = 10
        self.text_color = arcade.color.WHITE
        self.robot_info = {}

        self.sprites_total_height = 0

        self.sprites = arcade.SpriteList()

    def init_robot(self, name, sensors, bricks, side_bar_sprites):
        for sprite in side_bar_sprites:
            sprite.setup_visuals(self.x + self.width/2, self.y - self.sprites_total_height, 0.7)
            self.sprites_total_height += 110
            self.sprites.append(sprite)
        self.robot_info[name] = {}
        for address, sensor in sensors.items():
            self.robot_info[name][address] = {'name': sensor.name, 'value': None}

        for brick in bricks:
            self.robot_info[name][(brick.brick, 'speaker')] = {'name': f'{brick.name} sound', 'value': None}

    def add_robot_info(self, name, values, sounds):
        robot = self.robot_info[name]
        for address, value in values.items():
            robot[address]['value'] = value
        for address, sound in sounds.items():
            robot[address]['value'] = sound

    def draw(self):
        try:
            height = self.sprites_total_height
            for sprite in self.sprites:
                sprite.draw()
            for robot_name, sensorDict in self.robot_info.items():
                arcade.draw_text(robot_name, self.x + self.left_text_padding, self.y - height, self.text_color,
                                 self.text_size + 2, bold=True)
                height += (self.text_size + self.text_spacing)
                for address, sensor in sensorDict.items():
                    value = str(sensor['value'])
                    lines = value.count('\n')
                    height += (self.text_size * lines)
                    arcade.draw_text(f"{sensor['name']}: {value}", self.x + 2 * self.left_text_padding, self.y - height,
                                     self.text_color, self.text_size)
                    height += (self.text_size + self.text_spacing)
                height += (self.text_size + self.text_spacing)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
