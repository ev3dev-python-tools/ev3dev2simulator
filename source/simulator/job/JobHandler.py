from _queue import Empty
from queue import Queue

from source.simulator.job.MoveJob import MoveJob


class JobHandler:

    def __init__(self):
        self.left_move_queue = Queue()
        self.right_move_queue = Queue()


    def next_left_move_job(self) -> MoveJob:
        try:
            return self.left_move_queue.get_nowait()
        except Empty:
            return None


    def next_right_move_job(self) -> MoveJob:
        try:
            return self.right_move_queue.get_nowait()
        except Empty:
            return None


    def put_left_move_job(self, job):
        self.left_move_queue.put_nowait(job)


    def put_right_move_job(self, job):
        self.right_move_queue.put_nowait(job)


job_handler = JobHandler()


def get_job_handler():
    return job_handler
