from pathlib import Path

import yaml


class Config:
    """
    Class containing simulation configuration data.
    """


    def __init__(self):
        self.scale = None
        self.sim_type = None
        self.data = None


    def get_data(self):
        """
        Get configuration data. Initialize if data has not been initialized yet.
        :return: a data structure representing the configuration data.
        """

        if self.data is None:
            self.data = self._load_data()

        return self.data


    def get_scale(self) -> float:
        """
        Get scaling variable. Initialize if variable has not been initialized yet.
        :return: a floating point number representing the scaling multiplier.
        """

        if self.scale is None:
            self.scale = self._load_scale()

        return self.scale


    def get_sim_type(self) -> str:
        """
        Get simulation type variable. Initialize if variable has not been initialized yet.
        :return: a string representing the simulation type.
        """

        if self.sim_type is None:
            self.sim_type = self._load_sim_type()

        return self.sim_type


    def is_large_sim_type(self):
        return self.get_sim_type() == 'large'


    def _load_data(self):
        """
        Load config data from the correct config yaml file. The file to load from depends on the simulation type.
        :return: the config data.
        """

        file = 'config_large' if self.is_large_sim_type() else 'config_small'
        path = self.get_project_root() + '/' + file + '.yaml'

        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


    def _load_scale(self):
        """
        Load scale multiplier data from the scale_config.txt file.
        :return: a floating point number representing the scaling multiplier.
        """

        path = self.get_project_root() + '/scale_config.txt'

        with open(path, 'r') as stream:
            return float(stream.read(4))


    def _load_sim_type(self):
        """
        Load scale multiplier data from the type_config.txt file.
        :return: a string representing the simulation type.
        """

        path = self.get_project_root() + '/type_config.txt'

        with open(path, 'r') as stream:
            return stream.read(5)


    def write_scale(self, value: float):
        """
        Write the scaling multiplier to scale_config.txt
        :param value: a floating point number representing the scaling multiplier.
        """

        path = self.get_project_root() + '/scale_config.txt'

        with open(path, 'w') as stream:
            return stream.write(str(value))


    def write_sim_type(self, value: str):
        """
        Write the simulation type to type_config.txt
        :param value: a string representing the simulation type.
        """

        path = self.get_project_root() + '/type_config.txt'

        with open(path, 'w') as stream:
            return stream.write(value)


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
