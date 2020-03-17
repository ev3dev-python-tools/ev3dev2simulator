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
        self.text_color = arcade.color.WHITE
        self.robot_info = {}

    def init_robot(self, name, sensors, bricks):
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
        height = 170  # TODO check for robot arms
        for robot_name, sensorDict in self.robot_info.items():
            arcade.draw_text(robot_name, self.x, self.y - height, self.text_color, self.text_size, bold=True)
            height += (self.text_size + self.text_spacing)
            for address, sensor in sensorDict.items():
                value = str(sensor['value'])
                lines = value.count('\n')
                height += (self.text_size * lines)
                arcade.draw_text(f"{sensor['name']}: {value}", self.x, self.y - height,
                                 self.text_color, self.text_size)
                height += (self.text_size + self.text_spacing)

    # TODO add specifics for sensors
    # top_us = 'US  top:       ' + str(int(round(self.front_us_data / self.scaling_multiplier))) + 'mm'
    # bottom_us = 'US  bot:       ' + str(int(round(self.rear_us_data))) + 'mm'
    #
    #
    # arcade.draw_text('Sound:', self.text_x, self.screen_height - apply_scaling(210), arcade.color.WHITE, 10)
    # arcade.draw_text(sound, self.text_x, self.screen_height - apply_scaling(230), arcade.color.WHITE, 10,
    #                  anchor_y='top')
    #
    # arcade.draw_text('Robot Arm', apply_scaling(1450), self.screen_height - apply_scaling(50), arcade.color.WHITE,
    #                  14,
    #                  anchor_x="center")
    #
