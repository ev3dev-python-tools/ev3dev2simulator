from queue import Queue

from source.job.MoveJob import MoveJob
from source.job.RotateJob import RotateJob


class JobHandler:

    def __init__(self):
        self.move_queue = Queue()
        self.rotate_queue = Queue()

    def get_next_move_job(self) -> MoveJob:
        if self.move_queue.empty():
            return MoveJob(0, 0)
        else:
            return self.move_queue.get()

    def get_next_rotate_job(self) -> RotateJob:
        if self.rotate_queue.empty():
            return RotateJob(0)
        else:
            return self.rotate_queue.get()

    def put_move_job(self, job):
        self.move_queue.put(job)

    def put_rotate_job(self, job):
        self.rotate_queue.put(job)
