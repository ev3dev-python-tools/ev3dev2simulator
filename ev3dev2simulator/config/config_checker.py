"""
The config_checker module contains the class ConfigChecker. This class is ued to check the configs given to the sim.
"""

from strictyaml import Map, Str, Int, Float, CommaSeparated, Seq, Regex, Optional, Bool


class ConfigChecker:
    """
    Class containing all functions to check the different configuration files.
    """

    @staticmethod
    def check_world_config(world_config: object):
        """
        Checks for inconsistencies in world configurations
        """
        for robot in world_config['robots']:
            ConfigChecker.check_robot_config(robot)

    @staticmethod
    def check_robot_config(robot_config: object):
        """
        Checks for inconsistencies in world configurations
        """

    @staticmethod
    def get_robot_schema():
        """
        Getter for robot schema
        :return: schema that is used to verify the robot yaml
        """
        return Map({
            'parts': Seq(ConfigChecker.get_robot_part_schema())
        })

    @staticmethod
    def get_robot_part_schema():
        """
        Getter for robot schema
        :return: schema that is used to verify the robot yaml
        """
        return Map({
            'name': Str(),
            'type': Str(),
            'brick': Int(),
            'x_offset': Float(),
            'y_offset': Float(),
            Optional('port'): Regex('ev3-ports:(in[1-4]|out[A-D])'),
            Optional('side'): Regex('left|right|rear'),
            Optional('direction'): Regex('bottom|front'),
        })

    @staticmethod
    def get_world_schema():
        """
        Getter for world schema
        :return: schema that is used to verify the world yaml
        """
        return Map({
            'robots': Seq(
                Map({
                    'name': Str(),
                    'center_x': Int(),
                    'center_y': Int(),
                    'orientation': Int(),
                    Optional('type'): Str(),
                    Optional('parts'): Seq(ConfigChecker.get_robot_part_schema())
                })
            ),
            'board_height': Int(),
            'board_width': Int(),
            'board_color': CommaSeparated(Int()),
            'obstacles': Seq(
                Map({
                    'name': Str(),
                    'type': Str(),
                    Optional('outer_spacing'): Int(),
                    Optional('depth'): Int(),
                    Optional('color'): CommaSeparated(Int()),
                    Optional('border_width'): Int(),
                    Optional('inner_radius'): Int(),
                    Optional('x'): Int(),
                    Optional('y'): Int(),
                    Optional('width'): Int(),
                    Optional('height'): Int(),
                    Optional('angle'): Int(),
                    Optional('movable'): Bool(),
                    Optional('hole'): Bool(),
                    Optional('radius'): Int(),
                })
            ),
        })

    @staticmethod
    def get_settings_schema():
        """
        Getter for settings schema
        :return: schema that is used to verify the settings yaml
        """
        return Map({
            'screen_settings': Map({
                'background_color': CommaSeparated(Int()),
                'edge_spacing': Int(),
                'screen_height': Int(),
                'screen_width': Int(),
                'side_bar_width': Int(),
                'screen_title': Str(),
                'falling_message': Str()
            }),
            'image_paths': Map({
                'arm': Str(),
                'arm_large': Str(),
                'body': Str(),
                'color_sensor_black': Str(),
                'color_sensor_blue': Str(),
                'color_sensor_green': Str(),
                'color_sensor_red': Str(),
                'color_sensor_white': Str(),
                'color_sensor_yellow': Str(),
                'led_amber': Str(),
                'led_black': Str(),
                'led_green': Str(),
                'led_orange': Str(),
                'led_red': Str(),
                'led_yellow': Str(),
                'touch_sensor_left': Str(),
                'touch_sensor_rear': Str(),
                'touch_sensor_right': Str(),
                'ultrasonic_sensor_top': Str(),
                'ultrasonic_sensor_bottom': Str(),
                'wheel': Str()
            }),
            'body_part_sizes': Map({
                'body': Map({'width': Int(), 'height': Int()}),
                'arm': Map({'width': Int(), 'height': Int()}),
                'led': Map({'width': Int(), 'height': Int()}),
                'color_sensor': Map({'width': Int(), 'height': Int()}),
                'speaker': Map({'width': Int(), 'height': Int()}),
                'touch_sensor_bar': Map({'width': Int(), 'height': Int()}),
                'touch_sensor_bar_rear': Map({'width': Int(), 'height': Int()}),
                'ultrasonic_sensor_bottom': Map({'width': Int(), 'height': Int()}),
                'ultrasonic_sensor_top': Map({'width': Int(), 'height': Int()}),
                'wheel': Map({'width': Int(), 'height': Int()}),
            }),
            'exec_settings': Map({
                'frames_per_second': Int(),
                'socket_port': Int(),
                'bluetooth_port': Int(),
                'message_size': Int()
            }),
            'motor_settings': Map({
                'distance_coasting_subtraction': Float(),
                'degree_coasting_subtraction': Float()
            }),
            'wheel_settings': Map({'circumference': Float()})
        })
