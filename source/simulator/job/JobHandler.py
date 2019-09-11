from queue import Queue

from ev3dev2.util.Singleton import Singleton
from source.simulator.job.MoveJob import MoveJob


class JobHandler(metaclass=Singleton):

    def __init__(self):
        self.move_queue = Queue()

    def next_move_job(self) -> MoveJob:
        if self.move_queue.empty():
            return None
        else:
            return self.move_queue.get()

    def put_move_job(self, job):
        self.move_queue.put(job)
