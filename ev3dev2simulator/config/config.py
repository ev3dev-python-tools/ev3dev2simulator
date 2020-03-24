from pathlib import Path

import yaml

debug = False


class Config:
    """
    Class containing simulation configuration data.
    """

    def __init__(self):
        self.data = None

    def get_visualisation_config(self):
        """
        Get configuration data. Initialize if data has not been initialized yet.
        :return: a data structure representing the configuration data.
        """

        if self.data is None:
            self.data = self._load_data()

        return self.data

    def get_simulation_config(self, name):
        if name is None:
            name = 'config_large'
        return self._load_yaml_file(name)

    def _load_yaml_file(self, file_url):
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """

        path = self.get_project_root() + '/' + file_url + '.yaml'

        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise RuntimeError("there are errors in the yaml file")

    def _load_data(self):
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """
        file = 'visualisation'
        path = self.get_project_root() + '/' + file + '.yaml'

        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_project_root(self) -> str:
        """
        Get the absolute path to project root folder.
        :return: a string representing the path.
        """

        path = Path(__file__).parent
        return str(path)


config = Config()


def get_config() -> Config:
    return config
