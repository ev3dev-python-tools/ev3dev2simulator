from pathlib import Path
from os import listdir
from os.path import isfile, join
import yaml
import os


class Config:
    """
    Class containing simulation configuration data.
    """

    def __init__(self, world_config_file_name, orig_path = None):
        self.orig_path = orig_path
        self.rel_world_config_path = None
        self.world_config = self._load_world_config(world_config_file_name)
        self.simulation_settings = self._load_yaml_file('', 'simulation_settings')

    def _load_world_config(self, file_name: str):
        file_name = 'config_large' if file_name is None else file_name
        if os.path.dirname(file_name) != '':
            self.rel_world_config_path = os.path.dirname(file_name)
        return self._load_yaml_file('world_configurations', file_name, self.orig_path)

    def load_robot_config(self, file_name: str):
        """
        Loads a robot config.
        @param file_name: the file that contains the robot configuration.
        @return: dictionary with all the parts.
        """
        path = self.orig_path
        if self.rel_world_config_path:
            path = os.path.join(path, self.rel_world_config_path)
        return self._load_yaml_file('robot_configurations', file_name, path)

    @staticmethod
    def _load_yaml_file(prefix:str, file_url: str, orig_path: str = None) -> object:
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """
        mypath = f'{Config.get_project_root()}/{prefix}/'
        globalFiles = [f.replace('.yaml', '') for f in listdir(mypath) if isfile(join(mypath, f))]
        if file_url not in globalFiles:
            path = f'{orig_path}/{file_url}'
        else:
            path = f'{Config.get_project_root()}/{prefix}/{file_url}.yaml'
        try:
            with open(path, 'r') as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            raise FileNotFoundError(f'The configuration {path} could not be found')
        except yaml.YAMLError:
            raise RuntimeError('there are errors in the yaml file')


    @staticmethod
    def get_project_root() -> str:
        """
        Get the absolute path to project root folder.
        :return: a string representing the path.
        """
        path = Path(__file__).parent
        return str(path)


debug = False
production = True
_config = None


def load_config(world_config_file_name, orig_path = None):
    global _config

    if world_config_file_name == 'small':
        world_config_file_name = 'config_small'
    elif world_config_file_name == 'large':
        world_config_file_name = 'config_large'

    _config = Config(world_config_file_name, orig_path)

    return _config

def get_robot_config(file_name):
    return _config.load_robot_config(file_name)

def get_world_config():
    return _config.world_config


def get_simulation_settings():
    if not _config:  # clients might need configuration as well, but do not need world settings
        load_config(None)
    return _config.simulation_settings
