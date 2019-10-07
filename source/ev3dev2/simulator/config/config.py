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


def get_project_root() -> str:
    """
    Get the absolute path to project root folder.
    :return: a string representing the path.
    """

    path = Path(__file__).parent
    return str(path)
