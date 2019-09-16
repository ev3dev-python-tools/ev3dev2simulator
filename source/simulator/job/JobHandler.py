from _queue import Empty
from queue import Queue

from source.simulator.job.MoveJob import MoveJob


class JobHandler:

    def __init__(self):
        self.move_queue = Queue()

    def next_move_job(self) -> MoveJob:
        try:
            job = self.move_queue.get_nowait()
            # self.move_queue.task_done()

            print('GET2: ' + str(self.move_queue))
            return job
        except Empty:
            print('GET: ' + str(self.move_queue))
            return None

    def put_move_job(self, job):
        self.move_queue.put_nowait(job)
        # self.move_queue.task_done()
        print('PUT: ' + str(self.move_queue))


jh = JobHandler()


def get_job_handler():
    return jh;
