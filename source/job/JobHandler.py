from queue import Queue

from source.job.MoveJob import MoveJob


class JobHandler:

    def __init__(self):
        self.move_queue = Queue()

    def get_next_move_job(self) -> MoveJob:
        if self.move_queue.empty():
            return MoveJob(0, 0, 0)
        else:
            return self.move_queue.get()

    def put_move_job(self, job):
        self.move_queue.put(job)
