import os
import sys
import unittest
from io import StringIO
from contextlib import contextmanager

import ev3dev2simulator.Simulator as Simulator
from unittest.mock import patch, Mock, MagicMock


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestSimulator(unittest.TestCase):
    def test_default_parsing(self):
        args = vars(Simulator.parse_args([]))
        self.assertDictEqual(args,
                             {'version': False,
                              'simulation_file': 'config_small',
                              'show_on_second_monitor': False,
                              'fullscreen': False,
                              'maximized': False
                              })

    def test_single_dash_parsing(self):
        args = vars(Simulator.parse_args(['-V', '-t', 'config_test', '-2', '-f', '-m']))
        self.assertDictEqual(args,
                             {'version': True,
                              'simulation_file': 'config_test',
                              'show_on_second_monitor': True,
                              'fullscreen': True,
                              'maximized': True
                              })

    def test_double_dash_parsing(self):
        args = vars(Simulator.parse_args(['--version', '--simulation_file', 'config_test', '--show-on-second-monitor',
                                          '--fullscreen', '--maximized']))
        self.assertDictEqual(args,
                             {'version': True,
                              'simulation_file': 'config_test',
                              'show_on_second_monitor': True,
                              'fullscreen': True,
                              'maximized': True
                              })

    def test_main_print_version(self):
        testargs = ['name', '-V']
        with patch.object(sys, 'argv', testargs):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit):
                    Simulator.main()
            output = out.getvalue().strip()
            self.assertEqual(output, 'version ev3dev2           : 2.0.0beta5.post2\nversion ev3dev2simulator  : 1.3.2')

    def test_main(self):
        testargs = ['name']
        with patch.object(sys, 'argv', testargs):
            with patch('ev3dev2simulator.Simulator.Visualiser') as VisualiserMock:
                with patch('ev3dev2simulator.Simulator.start'):
                    with patch('ev3dev2simulator.Simulator.ServerSockets') as serverSocketsMock:
                        sockets_instance = serverSocketsMock.return_value
                        Simulator.main()

                        self.assertEqual(len(VisualiserMock.mock_calls), 1)
                        fn_name, args, kwargs = VisualiserMock.mock_calls[0]
                        self.assertEqual(fn_name, '')
                        self.assertEqual(args[2:], (False, False, False))  # the first two are functions

                        self.assertEqual(len(sockets_instance.mock_calls), 2)

                        fn_name, args, kwargs = sockets_instance.mock_calls[0]
                        self.assertEqual(fn_name, 'setDaemon')
                        self.assertEqual(args, (True,))

                        fn_name, args, kwargs = sockets_instance.mock_calls[1]
                        self.assertEqual(fn_name, 'start')
                        self.assertEqual(args, ())


if __name__ == '__main__':
    unittest.main()
