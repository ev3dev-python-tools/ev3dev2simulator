from pathlib import Path

import yaml


def load_config():
    """
    Load config data from config.yaml
    :return: the config data.
    """

    path = get_project_root() + '/config.yaml'

    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_scale_config() -> float:
    """
    Load scaling config data from scale_config.txt
    :return: a floating point number representing the scaling multiplier.
    """

    path = get_project_root() + '/scale_config.txt'

    with open(path, 'r') as stream:
        return float(stream.read(3))


def write_scale_config(value: float):
    """
    Write the scaling point multiplier to scale_config.txt
    :param value: a floating point number representing the scaling multiplier.
    """

    path = get_project_root() + '/scale_config.txt'

    with open(path, 'w') as stream:
        return stream.write(str(value))


def get_project_root() -> str:
    """
    Get the absolute path to project root folder.
    :return: a string representing the path.
    """

    path = Path(__file__).parent
    return str(path)
