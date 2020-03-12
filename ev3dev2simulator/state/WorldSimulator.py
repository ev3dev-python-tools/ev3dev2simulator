import threading
from queue import Queue, Empty
from typing import Any, Tuple

from ev3dev2simulator.config.config import get_config


class WorldSimulator:
    def __init__(self, world_state):
        self.objects = []
        self.robots = []

    def initialise(self):
        pass

    def update(self):
        pass

