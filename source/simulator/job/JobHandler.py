from _queue import Empty
from queue import Queue

from source.simulator.job.MoveJob import MoveJob


class JobHandler:

    def __init__(self):
        self.move_queue = Queue()

    def next_move_job(self) -> MoveJob:
        try:
            return self.move_queue.get_nowait()
        except Empty:
            return None

    def put_move_job(self, job):
        self.move_queue.put_nowait(job)


job_handler = JobHandler()


def get_job_handler():
    return job_handler
