import os
import unittest
from unittest.mock import MagicMock
from pathlib import Path
import ev3dev2simulator.config.config as conf
from ev3dev2simulator.visualisation.Visualiser import Visualiser

conf.load_config(None)


class TestVisualiser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        path = Path(os.path.realpath(__file__)).parent.parent.parent.parent.parent / 'ev3dev2simulator'
        os.chdir(path)

    def test_constructor(self):
        if conf.production:
            return

        world_state_mock = MagicMock()

        world_state_mock.board_height = 500
        world_state_mock.board_width = 500
        vis = Visualiser(lambda: None, world_state_mock, False, False, False)

    def test_update_current_screen(self):
        if conf.production:
            return

        world_state_mock = MagicMock()

        world_state_mock.board_height = 500
        world_state_mock.board_width = 500
        vis = Visualiser(lambda: None, world_state_mock, False, False, False)

        vis.update_current_screen()  # only checking if it does not crash at the moment
        vis.on_draw()


if __name__ == '__main__':
    unittest.main()
