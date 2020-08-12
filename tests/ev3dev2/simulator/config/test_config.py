import os
import unittest

import ev3dev2simulator.config.config as config

from unittest.mock import patch, MagicMock


class TestConfig(unittest.TestCase):

    def tearDown(self) -> None:
        config._config = None

    def test_load_config(self):
        with patch('ev3dev2simulator.config.config.Config') as ConfigMock:
            config.load_config('test_file')
            self.assertEqual(len(ConfigMock.mock_calls), 1)
            fn_name, args, kwargs = ConfigMock.mock_calls[0]
            self.assertEqual(args, ('test_file', None))

            config.load_config('small')

            self.assertEqual(len(ConfigMock.mock_calls), 2)
            fn_name, args, kwargs = ConfigMock.mock_calls[1]
            self.assertEqual(args, ('config_small', None))


            config.load_config('large')

            self.assertEqual(len(ConfigMock.mock_calls), 3)
            fn_name, args, kwargs = ConfigMock.mock_calls[2]
            self.assertEqual(args, ('config_large', None))

    def test_load_word_config(self):

        conf = config.Config(None)
        conf._load_yaml_file = MagicMock()
        conf._load_world_config(None)

        self.assertEqual(len(conf._load_yaml_file.mock_calls), 1)
        fn_name, args, kwargs = conf._load_yaml_file.mock_calls[0]
        self.assertEqual(args, ('world_configurations', 'config_large', None))

        conf._load_world_config('config_small')

        self.assertEqual(len(conf._load_yaml_file.mock_calls), 2)
        fn_name, args, kwargs = conf._load_yaml_file.mock_calls[1]
        self.assertEqual(args, ('world_configurations', 'config_small', None))


        conf = config.Config(None, 'test_path')
        conf._load_yaml_file = MagicMock()
        conf._load_world_config('local_config.yaml')

        self.assertEqual(len(conf._load_yaml_file.mock_calls), 1)
        fn_name, args, kwargs = conf._load_yaml_file.mock_calls[0]
        self.assertEqual(args, ('world_configurations', 'local_config.yaml', 'test_path'))


    def test_load_yaml_file(self):
        conf = config.Config(None)
        val = conf._load_yaml_file('world_configurations', 'config_small')
        self.assertEqual(val['board_height'], 841)
        conf._load_yaml_file('world_configurations', 'config_small2')
        conf._load_yaml_file('world_configurations', 'config_large')
        conf._load_yaml_file('world_configurations', 'config_large2')

        self.assertRaises(FileNotFoundError, conf._load_yaml_file, 'world_configurations', 'does_not_exist')

        with patch('ev3dev2simulator.config.config.Config.get_project_root') as ConfigMock:
            ConfigMock.return_value = str(os.path.dirname(__file__))
            self.assertRaises(RuntimeError, conf._load_yaml_file, 'world_configurations', 'config_small_error')


if __name__ == '__main__':
    unittest.main()
