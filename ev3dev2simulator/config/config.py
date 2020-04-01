from pathlib import Path

import yaml


class Config:
    """
    Class containing simulation configuration data.
    """

    def __init__(self, world_config_file_name):
        self.world_config = self._load_world_config(world_config_file_name)
        self.simulation_settings = self._load_yaml_file('simulation_settings')

    def _load_world_config(self, file_name: str):
        file_name = 'config_large' if file_name is None else file_name
        return self._load_yaml_file(f'world_configurations/{file_name}')

    @staticmethod
    def _load_yaml_file(file_url: str) -> object:
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """

        path = Config.get_project_root() + '/' + file_url + '.yaml'

        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise RuntimeError("there are errors in the yaml file")

    @staticmethod
    def get_project_root() -> str:
        """
        Get the absolute path to project root folder.
        :return: a string representing the path.
        """
        path = Path(__file__).parent
        return str(path)


debug = False
_config = None


def load_config(world_config_file_name):
    global _config

    if world_config_file_name == 'small':
        world_config_file_name = 'config_small'
    elif world_config_file_name == 'large':
        world_config_file_name = 'config_large'

    if _config is None:
        _config = Config(world_config_file_name)

    return _config


def get_world_config():
    return _config.world_config


def get_simulation_settings():
    return _config.simulation_settings
