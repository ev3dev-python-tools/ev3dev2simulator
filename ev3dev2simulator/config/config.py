"""
The module config contains all configuration file handling. Most of it is handled by the Config class.
"""

import os
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path

from strictyaml import load

from ev3dev2simulator.config.config_checker import ConfigChecker

THIS = sys.modules[__name__]


class Config:
    """
    Class containing simulation configuration data.
    """

    def __init__(self, world_config_file_name, orig_path=None):
        self.orig_path = orig_path
        self.rel_world_config_path = None
        world_config_yaml = self._load_world_config(world_config_file_name)
        ConfigChecker.check_world_config(world_config_yaml)
        self.world_config = world_config_yaml.data
        settings_schema = ConfigChecker.get_settings_schema()
        self.simulation_settings = self._load_yaml_file('', 'simulation_settings', None, settings_schema)

    def _load_world_config(self, file_name: str):
        file_name = 'config_large' if file_name is None else file_name
        if os.path.dirname(file_name) != '':
            self.rel_world_config_path = os.path.dirname(file_name)
        world_schema = ConfigChecker.get_world_schema()
        return self._load_yaml_file('world_configurations', file_name, self.orig_path, world_schema)

    def load_robot_config(self, file_name: str):
        """
        Loads a robot config.
        @param file_name: the file that contains the robot configuration.
        @return: dictionary with all the parts.
        """
        path = self.orig_path
        if self.rel_world_config_path:
            path = os.path.join(path, self.rel_world_config_path)
        robot_schema = ConfigChecker.get_robot_schema()
        robot_config_yaml = self._load_yaml_file('robot_configurations', file_name, path, robot_schema)
        ConfigChecker.check_robot_config(robot_config_yaml)
        return robot_config_yaml.data

    @staticmethod
    def _load_yaml_file(prefix: str, file_url: str, orig_path: str = None, schema=None) -> object:
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """
        my_path = f'{Config.get_project_root()}/{prefix}/'
        global_files = [f.replace('.yaml', '') for f in listdir(my_path) if isfile(join(my_path, f))]
        if file_url not in global_files:
            path = f'{orig_path}/{file_url}'
        else:
            path = f'{Config.get_project_root()}/{prefix}/{file_url}.yaml'
        try:
            with open(path) as stream:
                return load(stream.read(), schema, path)
        except FileNotFoundError:
            raise FileNotFoundError(f'The configuration {path} could not be found')

    @staticmethod
    def get_project_root() -> str:
        """
        Get the absolute path to project root folder.
        :return: a string representing the path.
        """
        path = Path(__file__).parent
        return str(path)


DEBUG = False
PRODUCTION = True
THIS.CONFIG = None


def load_config(world_config_file_name, orig_path=None):
    """
    Loads the world config.
    """
    if world_config_file_name == 'small':
        world_config_file_name = 'config_small'
    elif world_config_file_name == 'large':
        world_config_file_name = 'config_large'

    THIS.CONFIG = Config(world_config_file_name, orig_path)

    return THIS.CONFIG


def get_robot_config(file_name):
    """
    Gets robots config by name.
    """
    return THIS.CONFIG.load_robot_config(file_name)


def get_world_config():
    """
    Get the current world config
    """
    return THIS.CONFIG.world_config


def get_simulation_settings():
    """
    Singleton function creating a configuration if it does not exist, and return the instance of the config class.
    """
    if not THIS.CONFIG:  # clients might need configuration as well, but do not need world settings
        load_config(None)
    return THIS.CONFIG.simulation_settings.data
